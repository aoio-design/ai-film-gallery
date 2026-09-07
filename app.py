"""
CONSUME Gallery — 5-row shot viewer for Lucas's AI film pipeline.

Rows per shot:
1. Script segment
2. Image prompt (editable)
3. Generated image
4. Video prompt (editable)
5. Generated video
+ Feedback section

Auth: email + password (AOIO account store) via session cookie.
"""
import json, os, re, sys, uuid, shutil, secrets, time, hmac
from pathlib import Path
from datetime import datetime, timezone
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, session,
    url_for, send_from_directory, jsonify, abort
)

# Shared account store (stdlib-only module, so it works in any venv).
# Looked up in this order: $AOIO_AUTH_DIR, ./accounts next to this file
# (how the public repo ships it), then /opt/data/aoio-auth.
def _find_account_store():
    here = Path(__file__).resolve().parent
    for cand in (os.environ.get("AOIO_AUTH_DIR"), str(here / "accounts"), "/opt/data/aoio-auth"):
        if cand and (Path(cand) / "aoio_auth.py").is_file():
            return cand
    raise SystemExit("aoio_auth.py not found — set AOIO_AUTH_DIR to the folder holding it")

sys.path.insert(0, _find_account_store())
import aoio_auth

app = Flask(__name__)
# Stable across restarts when GALLERY_SECRET is set, so a restart does not sign
# everyone out; random (sessions dropped on restart) when it is not.
app.secret_key = os.environ.get("GALLERY_SECRET") or os.urandom(32).hex()
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # Set GALLERY_SECURE_COOKIE=1 when the gallery is only reached over HTTPS
    # (e.g. behind a Cloudflare tunnel). Leave it off while testing on
    # http://127.0.0.1, or the browser will refuse to send the cookie.
    SESSION_COOKIE_SECURE=os.environ.get("GALLERY_SECURE_COOKIE", "") == "1",
)


@app.after_request
def _no_cache_html(response):
    """Prevent Cloudflare from caching HTML pages so CSS/JS changes go live
    immediately on hard refresh."""
    if response.content_type and response.content_type.startswith("text/html"):
        response.headers["Cache-Control"] = "no-store, max-age=0"
    return response


# --- Config ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SHOTS_DIR = BASE_DIR / "shots"
PROJECTS_FILE = DATA_DIR / "projects.json"

# First-run setup only. NO password is shipped in this file or in start.sh: while
# zero accounts exist the app generates a random one-time setup code per start and
# prints it to its log (gallery.log). Anyone reading this source learns nothing
# usable. The code stops working the moment an account exists.
_SETUP_CODE = None
# Roles allowed to open the studio.
GALLERY_ROLES = ("owner", "reviewer")
# Failed-login throttle: attempts per IP per window (seconds).
LOGIN_MAX_FAILS, LOGIN_WINDOW = 10, 300
_login_fails = {}


def setup_code():
    """Random one-time setup code, valid only while no account exists."""
    global _SETUP_CODE
    if _SETUP_CODE is None:
        _SETUP_CODE = "setup-" + secrets.token_urlsafe(9)
        print(f"[gallery] no accounts yet — one-time setup code: {_SETUP_CODE}\n"
              f"[gallery] create your real login with: "
              f"python3 aoio_auth.py add you@example.com", flush=True)
    return _SETUP_CODE


def client_ip():
    """Caller IP for throttling. Only CF-Connecting-IP (set by Cloudflare, not
    forgeable by the client) is trusted; otherwise the socket address. Never
    X-Forwarded-For, which any client can send."""
    return request.headers.get("CF-Connecting-IP") or request.remote_addr or "?"


def login_throttled(ip):
    now = time.time()
    hits = [t for t in _login_fails.get(ip, []) if now - t < LOGIN_WINDOW]
    _login_fails[ip] = hits
    if len(_login_fails) > 5000:          # bound memory against spoofed-IP floods
        _login_fails.clear()
    return len(hits) >= LOGIN_MAX_FAILS


def login_failed(ip):
    _login_fails.setdefault(ip, []).append(time.time())

DATA_DIR.mkdir(parents=True, exist_ok=True)
SHOTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Auth ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated

# --- Data helpers ---
def load_projects():
    if PROJECTS_FILE.exists():
        return json.loads(PROJECTS_FILE.read_text())
    return {"projects": []}

def load_seasons(data=None):
    data = data or load_projects()
    return data.get("seasons", [])

def get_season_for_episode(episode_id, data=None):
    for s in load_seasons(data):
        if episode_id in s.get("episodes", []):
            return s
    return None

def save_projects(data):
    PROJECTS_FILE.write_text(json.dumps(data, indent=2))

def get_shot_dir(project_id, shot_id):
    return SHOTS_DIR / project_id / shot_id

def _pick_newest(files, d):
    """Display default when nothing is approved yet: the most recently
    generated/uploaded file (regeneration order == file mtime)."""
    best, best_t = None, -1.0
    for name in files:
        try:
            t = (d / name).stat().st_mtime
        except OSError:
            t = 0.0
        if t > best_t:
            best_t, best = t, name
    return best

def _mtime_of(d, name):
    try:
        return (d / name).stat().st_mtime
    except OSError:
        return 0.0

def _primary_valid(meta, key, files, d):
    """Is the stored approval still valid? An approval describes a specific
    media state, so any regeneration invalidates it:
      - a newer file of the same kind arrived (additive regeneration), or
      - the approved file itself was rewritten in place after approval.
    Approving touches the file (making it the newest) and records *_at, so a
    deliberate pick of an older file sticks until the NEXT regeneration."""
    p = meta.get(key)
    if not p or p not in files:
        return False
    pt = _mtime_of(d, p)
    if any(_mtime_of(d, f) > pt for f in files):
        return False
    at = meta.get(key + "_at")
    if at:
        try:
            t = datetime.fromisoformat(at).timestamp()
        except Exception:
            t = None
        if t is not None and pt > t + 5:
            return False
    return True

def get_shot_meta(project_id, shot_id):
    d = get_shot_dir(project_id, shot_id)
    meta_file = d / "metadata.json"
    if meta_file.exists():
        try:
            return json.loads(meta_file.read_text())
        except Exception:
            bak = meta_file.with_suffix(".json.bak")
            if bak.exists():
                try:
                    meta = json.loads(bak.read_text())
                    meta_file.write_text(json.dumps(meta, indent=2))
                    return meta
                except Exception:
                    pass
            return {}
    return {}

def save_shot_meta(project_id, shot_id, meta):
    d = get_shot_dir(project_id, shot_id)
    d.mkdir(parents=True, exist_ok=True)
    meta_file = d / "metadata.json"
    if meta_file.exists():
        try:
            (d / "metadata.json.bak").write_text(meta_file.read_text())
        except Exception:
            pass
    meta_file.write_text(json.dumps(meta, indent=2))

# --- Routes ---

@app.route("/")
def index():
    return redirect(url_for("project_list"))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    error = None
    # First-run mode: no accounts yet -> accept the random one-time setup code
    # printed to gallery.log, so a fresh install is reachable before the first
    # account is created. Disappears the moment an account exists.
    bootstrap = aoio_auth.count_users() == 0
    if request.method == "POST":
        ip = client_ip()
        if login_throttled(ip):
            return render_template(
                "login.html", bootstrap=bootstrap,
                error="Too many attempts. Try again in a few minutes."), 429
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if bootstrap and not email:
            if hmac.compare_digest(password, setup_code()):
                session["logged_in"] = True
                session["email"] = "setup"
                return redirect(url_for("project_list"))
            login_failed(ip)
            error = "Wrong setup code"
        else:
            user = aoio_auth.verify(email, password, roles=GALLERY_ROLES)
            if user:
                session["logged_in"] = True
                session["email"] = user["email"]
                session["name"] = user["name"]
                session["role"] = user["role"]
                return redirect(url_for("project_list"))
            login_failed(ip)
            print(f"[gallery] login REJECTED for {email or '-'} from {ip}", flush=True)
            error = "Wrong email or password"
    elif bootstrap:
        setup_code()          # make sure the code is generated + logged
    return render_template("login.html", error=error, bootstrap=bootstrap)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/projects")
@login_required
def project_list():
    data = load_projects()
    seasons = load_seasons(data)
    if seasons:
        # Season list: each season shows its episode count + assets link
        for s in seasons:
            s["episode_count"] = len(s.get("episodes", []))
            s["has_assets"] = (APP_ASSETS_DIR / s["id"]).exists()
        return render_template("project_list.html", seasons=seasons, projects=[])
    return render_template("project_list.html", seasons=[], projects=data["projects"])

@app.route("/s/<season_id>")
@login_required
def season_page(season_id):
    data = load_projects()
    season = next((s for s in load_seasons(data) if s["id"] == season_id), None)
    if not season:
        abort(404)
    episodes = []
    for ep_id in season.get("episodes", []):
        ep = next((p for p in data["projects"] if p["id"] == ep_id), None)
        if ep:
            episodes.append({"id": ep["id"], "title": ep.get("title", ep["id"]), "shots": len(ep.get("shots", []))})
    season["episodes"] = episodes
    season["has_assets"] = (APP_ASSETS_DIR / season_id).exists()
    return render_template("season.html", season=season)

@app.route("/p/<project_id>")
@login_required
def gallery(project_id):
    data = load_projects()
    project = None
    for p in data["projects"]:
        if p["id"] == project_id:
            project = p
            break
    if not project:
        abort(404)

    # Load shot metadata
    # Multi-file media support (regeneration history): all images/videos in the
    # shot dir, with a user-selectable "primary" per kind shown by default.
    IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
    VIDEO_EXTS = (".mp4", ".webm", ".mov")

    def list_shot_media(project_id, shot_id):
        """(image_filenames, video_filenames) sorted naturally-ish."""
        sd = get_shot_dir(project_id, shot_id)
        images, videos = [], []
        if sd.exists():
            for f in sorted(sd.iterdir()):
                if not f.is_file() or f.name == "metadata.json":
                    continue
                n = f.name.lower()
                if n.endswith(IMAGE_EXTS):
                    images.append(f.name)
                elif n.endswith(VIDEO_EXTS):
                    videos.append(f.name)
        return images, videos

    def _natural(s):
        return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]

    for shot in project["shots"]:
        meta = get_shot_meta(project_id, shot["id"])
        shot["script"] = meta.get("script", "")
        shot["image_prompt"] = meta.get("image_prompt", "")
        shot["video_prompt"] = meta.get("video_prompt", "")
        shot["feedback"] = meta.get("feedback", [])
        images, videos = list_shot_media(project_id, shot["id"])
        images.sort(key=_natural)
        videos.sort(key=_natural)
        shot["images"] = images
        shot["videos"] = videos
        # Approval state (the star): only an explicit stored pick counts, and
        # only while the media set is unchanged. Nothing is auto-approved, and
        # a regeneration (any newer file, or the approved file rewritten in
        # place) automatically reverts the pick to unapproved.
        sd = get_shot_dir(project_id, shot["id"])
        dirty = False
        if meta.get("primary_image") and (meta.get("primary_image") not in images
                or not _primary_valid(meta, "primary_image", images, sd)):
            meta.pop("primary_image", None); meta.pop("primary_image_at", None); dirty = True
        if meta.get("primary_video") and (meta.get("primary_video") not in videos
                or not _primary_valid(meta, "primary_video", videos, sd)):
            meta.pop("primary_video", None); meta.pop("primary_video_at", None); dirty = True
        if dirty:
            save_shot_meta(project_id, shot["id"], meta)
        shot["primary_image"] = meta.get("primary_image") if meta.get("primary_image") in images else None
        shot["primary_video"] = meta.get("primary_video") if meta.get("primary_video") in videos else None
        # Display default for the preview box / player: the approved file if
        # any, otherwise the NEWEST file (regenerated clips surface latest).
        shot["fallback_image"] = _pick_newest(images, sd)
        shot["fallback_video"] = _pick_newest(videos, sd)
        shot["preview_image"] = shot["primary_image"] or shot["fallback_image"]
        shot["preview_video"] = shot["primary_video"] or shot["fallback_video"]
        shot["has_image"] = bool(images)
        shot["has_video"] = bool(videos)

    # Episode script: use the saved editable copy if it exists, else assemble
    # from each shot's script field (with [ShotID] markers for orientation).
    ep_file = SHOTS_DIR / project_id / "_episode_script.json"
    episode = {"text": "", "feedback": []}
    if ep_file.exists():
        try:
            episode = json.loads(ep_file.read_text())
        except Exception:
            episode = {"text": "", "feedback": []}
    if not episode.get("text"):
        parts = []
        for shot in project["shots"]:
            s = (shot.get("script") or "").strip()
            if s:
                parts.append(f"[{shot['id']}]\n{s}")
        episode["text"] = "\n\n".join(parts) or "(no script yet)"
    episode.setdefault("feedback", [])

    season = get_season_for_episode(project_id)
    return render_template("gallery.html", project=project, episode=episode, season=season)

@app.route("/p/<project_id>/script", methods=["POST"])
@login_required
def save_episode_script(project_id):
    text = request.form.get("text", "")
    f = SHOTS_DIR / project_id / "_episode_script.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if f.exists():
        try:
            data = json.loads(f.read_text())
        except Exception:
            data = {}
    data["text"] = text
    f.write_text(json.dumps(data, indent=2))
    return jsonify({"ok": True})

@app.route("/p/<project_id>/script_feedback", methods=["POST"])
@login_required
def add_episode_script_feedback(project_id):
    text = request.form.get("text", "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Empty feedback"}), 400
    f = SHOTS_DIR / project_id / "_episode_script.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if f.exists():
        try:
            data = json.loads(f.read_text())
        except Exception:
            data = {}
    data.setdefault("feedback", []).append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text": text
    })
    if "text" not in data:
        data["text"] = ""
    f.write_text(json.dumps(data, indent=2))
    return jsonify({"ok": True})

@app.route("/p/<project_id>/<shot_id>/file/<filename>")
@login_required
def shot_file(project_id, shot_id, filename):
    d = get_shot_dir(project_id, shot_id)
    if not d.exists():
        abort(404)
    return send_from_directory(str(d), filename)

@app.route("/p/<project_id>/<shot_id>/update", methods=["POST"])
@login_required
def update_shot(project_id, shot_id):
    meta = get_shot_meta(project_id, shot_id)
    field = request.form.get("field")
    value = request.form.get("value", "")
    if field in ("image_prompt", "video_prompt", "script", "primary_image", "primary_video"):
        # Empty value clears the field (unapproving removes the stored pick)
        if not value:
            meta.pop(field, None)
            meta.pop(field + "_at", None)
        else:
            meta[field] = value
            if field.startswith("primary_"):
                # Timestamp + touch the file: an approval is only valid while
                # the media set is unchanged, so regenerations are detectable.
                meta[field + "_at"] = datetime.now(timezone.utc).isoformat()
                if "/" not in value and "\\" not in value:
                    try:
                        os.utime(get_shot_dir(project_id, shot_id) / value)
                    except OSError:
                        pass
        save_shot_meta(project_id, shot_id, meta)
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Unknown field"}), 400


@app.route("/p/<project_id>/<shot_id>/upload", methods=["POST"])
@login_required
def upload_shot_media(project_id, shot_id):
    """Add one or more generated images/videos to a shot (regeneration history).

    Existing files are never overwritten — a name collision gets a numeric
    suffix (image.png -> image-2.png). Nothing is auto-approved: new media
    starts unapproved until the owner picks it with the star.
    """
    d = get_shot_dir(project_id, shot_id)
    d.mkdir(parents=True, exist_ok=True)
    IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
    VIDEO_EXTS = (".mp4", ".webm", ".mov")
    saved, skipped = [], []
    for f in request.files.getlist("files"):
        name = (f.filename or "").strip()
        if not name:
            continue
        base = os.path.basename(name).replace(" ", "-")
        stem, ext = os.path.splitext(base)
        ext = ext.lower()
        if ext not in IMAGE_EXTS + VIDEO_EXTS:
            skipped.append(base)
            continue
        candidate = stem + ext
        n = 2
        while (d / candidate).exists():
            candidate = f"{stem}-{n}{ext}"
            n += 1
        f.save(str(d / candidate))
        saved.append(candidate)
    # A regeneration (new files landing) invalidates any previous approval of
    # that kind — the pick must be made again on the new media.
    meta = get_shot_meta(project_id, shot_id)
    dirty = False
    if any(os.path.splitext(s)[1].lower() in IMAGE_EXTS for s in saved) and meta.get("primary_image"):
        meta.pop("primary_image", None); meta.pop("primary_image_at", None); dirty = True
    if any(os.path.splitext(s)[1].lower() in VIDEO_EXTS for s in saved) and meta.get("primary_video"):
        meta.pop("primary_video", None); meta.pop("primary_video_at", None); dirty = True
    if dirty:
        save_shot_meta(project_id, shot_id, meta)
    return jsonify({"ok": True, "saved": saved, "skipped": skipped})


def ext_group(filename, image_exts, video_exts):
    n = filename.lower()
    for e in image_exts:
        if n.endswith(e):
            return "image"
    for e in video_exts:
        if n.endswith(e):
            return "video"
    return "other"


@app.route("/agent_feedback", methods=["POST"])
@login_required
def agent_feedback():
    """Unified "Talk to your agent" feedback from the studio drawer.

    Auto-tagged with where the user was when they wrote it (project, section,
    shot / asset) plus the visible text of that context, so the agent gets
    "script, lines 13-15" style grounding without the user typing it.
    Appends to the SAME per-target feedback files the watcher reads.
    FULL DESIGN NOTES for this loop: see docs/FAB-DESIGN.md in this repo.
    """
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Empty feedback"}), 400
    ctx = data.get("context") or {}
    project_id = ctx.get("project")
    target = ctx.get("target")          # 'episode' | 'shot' | 'asset' | None
    ident = ctx.get("id")
    section = ctx.get("section")        # 'Episode Script' | 'Video Preview' | 'Shot List' | 'Assets'
    label = ctx.get("label") or ""

    stamp = datetime.now(timezone.utc).isoformat()
    entry_text = text
    if section:
        entry_text = f"[{section}" + (f" · {label}]" if label else "]") + f" {text}"

    written = None
    if target == "episode" and project_id:
        f = SHOTS_DIR / project_id / "_episode_script.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        d = {}
        if f.exists():
            try:
                d = json.loads(f.read_text())
            except Exception:
                d = {}
        d.setdefault("feedback", []).append({"timestamp": stamp, "text": entry_text})
        if "text" not in d:
            d["text"] = ""
        f.write_text(json.dumps(d, indent=2))
        written = f"{project_id}/_episode_script.json"
    elif target == "shot" and project_id and ident:
        meta = get_shot_meta(project_id, ident)
        meta.setdefault("feedback", []).append({"timestamp": stamp, "text": entry_text})
        save_shot_meta(project_id, ident, meta)
        written = f"{project_id}/{ident}/metadata.json"
    elif target == "asset" and project_id and ident:
        meta = get_asset_meta(project_id, ident)
        meta.setdefault("feedback", []).append({"timestamp": stamp, "text": entry_text})
        save_asset_meta(project_id, ident, meta)
        written = f"assets/{project_id}/{ident}/metadata.json"
    else:
        # No specific target — park it in a studio-wide inbox the watcher covers
        # by convention (shots/_studio_feedback.json).
        f = SHOTS_DIR / "_studio_feedback.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        d = []
        if f.exists():
            try:
                d = json.loads(f.read_text())
            except Exception:
                d = []
        d.append({"timestamp": stamp, "text": entry_text})
        f.write_text(json.dumps(d, indent=2))
        written = "_studio_feedback.json"

    print(f"[studio] agent feedback ({written}): {text[:120]}", flush=True)
    return jsonify({"ok": True, "written": written})

@app.route("/agent_replies", methods=["GET"])
@login_required
def agent_replies():
    """Agent replies to the owner's feedback, shown in the studio drawer.

    The background feedback watcher (agent-mode cron) writes its actions/replies
    to SHOTS_DIR/_agent_replies.json as a list. The drawer polls this endpoint
    and displays any new replies. Optionally filter by ?project=.
    FULL DESIGN NOTES for this loop: see docs/FAB-DESIGN.md in this repo.
    """
    f = SHOTS_DIR / "_agent_replies.json"
    replies = []
    if f.exists():
        try:
            replies = json.loads(f.read_text(encoding="utf-8"))
            if not isinstance(replies, list):
                replies = []
        except Exception:
            replies = []
    project = (request.args.get("project") or "").strip()
    if project:
        # Keep replies for THIS project AND general replies (no specific project),
        # so a project-scoped page still shows notes the agent answered generally.
        replies = [r for r in replies if (r.get("project") or "") == project
                   or not (r.get("project") or "").strip()]
    # Newest first
    replies.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return jsonify({"replies": replies})

@app.route("/p/<project_id>/<shot_id>/feedback", methods=["POST"])
@login_required
def add_feedback(project_id, shot_id):
    meta = get_shot_meta(project_id, shot_id)
    text = request.form.get("text", "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Empty feedback"}), 400
    if "feedback" not in meta:
        meta["feedback"] = []
    meta["feedback"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text": text
    })
    save_shot_meta(project_id, shot_id, meta)
    return jsonify({"ok": True})

APP_ASSETS_DIR = BASE_DIR / "assets"

def get_asset_meta(project_id, asset_id):
    f = APP_ASSETS_DIR / project_id / asset_id / "metadata.json"
    if f.exists():
        try:
            return json.loads(f.read_text())
        except Exception:
            # Corrupt file: try the backup instead of returning {} (which would let
            # the next read-modify-write silently wipe all other fields).
            bak = f.with_suffix(".json.bak")
            if bak.exists():
                try:
                    meta = json.loads(bak.read_text())
                    f.write_text(json.dumps(meta, indent=2))
                    return meta
                except Exception:
                    pass
            return {}
    return {}

def save_asset_meta(project_id, asset_id, meta):
    d = APP_ASSETS_DIR / project_id / asset_id
    d.mkdir(parents=True, exist_ok=True)
    f = d / "metadata.json"
    if f.exists():
        try:
            (d / "metadata.json.bak").write_text(f.read_text())
        except Exception:
            pass
    f.write_text(json.dumps(meta, indent=2))

def _billing(role):
    """Billing order for the Character Bible: leads first, then supporting."""
    r = (role or "").strip().lower()
    if r.startswith("lead") or r.startswith("main") or r.startswith("protagonist"):
        return 0
    if r.startswith("support") or r.startswith("supporting"):
        return 1
    return 2

@app.route("/a/<assets_scope>")
@login_required
def assets_page(assets_scope):
    data = load_projects()
    scope_title = assets_scope
    # Prefer a season scope; fall back to a project scope.
    season = next((s for s in load_seasons(data) if s["id"] == assets_scope), None)
    if season:
        scope_title = season.get("title", assets_scope)
    else:
        proj = next((p for p in data["projects"] if p["id"] == assets_scope), None)
        if proj:
            scope_title = proj.get("title", assets_scope)
    assets = []
    adir = APP_ASSETS_DIR / assets_scope
    if adir.exists():
        for d in sorted(adir.iterdir()):
            if not d.is_dir() or d.name.startswith("."):
                continue
            meta = get_asset_meta(assets_scope, d.name)
            files = sorted(f.name for f in d.iterdir() if f.is_file() and f.name != "metadata.json")
            images = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
            audios = [f for f in files if f.lower().endswith((".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"))]
            # A regeneration (any newer image, or the approved one rewritten in
            # place) reverts the asset to unapproved; keep the file in step.
            if meta.get("primary_image") and (meta.get("primary_image") not in images
                    or not _primary_valid(meta, "primary_image", images, d)):
                meta.pop("primary_image", None)
                meta.pop("primary_image_at", None)
                meta["status"] = "Generated"
                save_asset_meta(assets_scope, d.name, meta)
            pi = meta.get("primary_image")
            assets.append({
                "id": d.name,
                "name": meta.get("name", d.name),
                "type": meta.get("type", ""),
                "role": meta.get("role", ""),
                "billing": _billing(meta.get("role", "")),
                "appearance": meta.get("appearance", ""),
                "personality": meta.get("personality", ""),
                "distinguishing": meta.get("distinguishing", ""),
                "wardrobe": meta.get("wardrobe", ""),
                "emotional_range": meta.get("emotional_range", ""),
                "body_language": meta.get("body_language", ""),
                "voice": meta.get("voice", ""),
                "character_sheet_prompt": meta.get("character_sheet_prompt", ""),
                "voice_prompt": meta.get("voice_prompt", ""),
                "status": _asset_status(pi, images),
                "description": meta.get("description", ""),
                "prompt": meta.get("prompt", ""),
                "feedback": meta.get("feedback", []),
                "image": images[0] if images else None,
                "primary_image": pi if pi in images else None,
                "audio": audios[0] if audios else None,
                "images": images,
                "audios": audios,
            })
    # Leads/main characters first, then supporting, then non-characters (stable, so
    # the Location/Prop table keeps its alphabetical order).
    assets.sort(key=lambda a: (a["billing"], a["name"].lower()))
    return render_template("assets.html", scope_id=assets_scope, scope_title=scope_title, assets=assets, season=season)

def _asset_status(pi, images):
    """Pill label = image-approval state ONLY (derived from the star):
    an approved (stored) image -> "Approved"; reference images exist but none
    approved -> "Generated"; no reference images -> hidden ("")."""
    if not images:
        return ""
    return "Approved" if pi in images else "Generated"

@app.route("/a/<project_id>/<asset_id>/file/<filename>")
@login_required
def asset_file(project_id, asset_id, filename):
    d = APP_ASSETS_DIR / project_id / asset_id
    if not d.exists():
        abort(404)
    return send_from_directory(str(d), filename)

@app.route("/a/<project_id>/<asset_id>/update", methods=["POST"])
@login_required
def update_asset(project_id, asset_id):
    meta = get_asset_meta(project_id, asset_id)
    field = request.form.get("field")
    value = request.form.get("value", "")
    if field in ("name", "type", "role", "appearance", "personality", "distinguishing",
                 "wardrobe", "emotional_range", "body_language", "voice", "status",
                 "description", "prompt", "character_sheet_prompt", "voice_prompt",
                 "primary_image"):
        # Empty value clears the field (unapproving removes the stored pick)
        if not value:
            meta.pop(field, None)
            meta.pop(field + "_at", None)
        else:
            meta[field] = value
            if field == "primary_image":
                # Timestamp + touch the file: an approval is only valid while
                # the media set is unchanged, so regenerations are detectable.
                meta["primary_image_at"] = datetime.now(timezone.utc).isoformat()
                if "/" not in value and "\\" not in value:
                    try:
                        os.utime(APP_ASSETS_DIR / project_id / asset_id / value)
                    except OSError:
                        pass
        # Keep the stored status field in step with the star (agents read the
        # metadata files directly; the pill itself is derived at render time).
        pi = meta.get("primary_image")
        d = APP_ASSETS_DIR / project_id / asset_id
        if pi and "/" not in pi and "\\" not in pi and (d / pi).is_file():
            meta["status"] = "Approved"
        else:
            meta["status"] = "Generated"
        save_asset_meta(project_id, asset_id, meta)
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Unknown field"}), 400

@app.route("/a/<project_id>/<asset_id>/feedback", methods=["POST"])
@login_required
def add_asset_feedback(project_id, asset_id):
    text = request.form.get("text", "").strip()
    if not text:
        return jsonify({"ok": False, "error": "Empty feedback"}), 400
    meta = get_asset_meta(project_id, asset_id)
    meta.setdefault("feedback", []).append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text": text
    })
    save_asset_meta(project_id, asset_id, meta)
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("GALLERY_PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
