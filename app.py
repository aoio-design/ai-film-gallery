"""
CONSUME Gallery — 5-row shot viewer for Lucas's AI film pipeline.

Rows per shot:
1. Script segment
2. Image prompt (editable)
3. Generated image
4. Video prompt (editable)
5. Generated video
+ Feedback section

Auth: single password via session cookie.
"""
import json, os, uuid, shutil
from pathlib import Path
from datetime import datetime, timezone
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, session,
    url_for, send_from_directory, jsonify, abort
)

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()

# --- Config ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SHOTS_DIR = BASE_DIR / "shots"
PROJECTS_FILE = DATA_DIR / "projects.json"

GALLERY_PASSWORD = os.environ.get("GALLERY_PASSWORD", "consume2026")

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

def get_shot_meta(project_id, shot_id):
    d = get_shot_dir(project_id, shot_id)
    meta_file = d / "metadata.json"
    if meta_file.exists():
        return json.loads(meta_file.read_text())
    return {}

def save_shot_meta(project_id, shot_id, meta):
    d = get_shot_dir(project_id, shot_id)
    d.mkdir(parents=True, exist_ok=True)
    (d / "metadata.json").write_text(json.dumps(meta, indent=2))

# --- Routes ---

@app.route("/")
def index():
    return redirect(url_for("project_list"))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    error = None
    if request.method == "POST":
        if request.form.get("password") == GALLERY_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("project_list"))
        error = "Wrong password"
    return render_template("login.html", error=error)

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
    for shot in project["shots"]:
        meta = get_shot_meta(project_id, shot["id"])
        shot["script"] = meta.get("script", "")
        shot["image_prompt"] = meta.get("image_prompt", "")
        shot["video_prompt"] = meta.get("video_prompt", "")
        shot["feedback"] = meta.get("feedback", [])
        shot["audio_note"] = meta.get("audio_note", "")
        shot["expected_audio"] = meta.get("expected_audio", [])
        # Check if image/video files exist
        sd = get_shot_dir(project_id, shot["id"])
        shot["has_image"] = any(f.name in ("image.png", "image.jpg") for f in sd.iterdir()) if sd.exists() else False
        shot["has_video"] = any(f.suffix in (".mp4", ".webm", ".mov") for f in sd.iterdir()) if sd.exists() else False
        # Audio files (multiple supported) — sorted by filename
        audio_ext = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac")
        shot["audio_files"] = sorted(
            [f.name for f in sd.iterdir() if f.suffix.lower() in audio_ext]
        ) if sd.exists() else []

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
    if field in ("image_prompt", "video_prompt", "script"):
        meta[field] = value
        save_shot_meta(project_id, shot_id, meta)
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Unknown field"}), 400

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
            return {}
    return {}

def save_asset_meta(project_id, asset_id, meta):
    d = APP_ASSETS_DIR / project_id / asset_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "metadata.json").write_text(json.dumps(meta, indent=2))

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
            assets.append({
                "id": d.name,
                "name": meta.get("name", d.name),
                "type": meta.get("type", ""),
                "role": meta.get("role", ""),
                "appearance": meta.get("appearance", ""),
                "personality": meta.get("personality", ""),
                "distinguishing": meta.get("distinguishing", ""),
                "wardrobe": meta.get("wardrobe", ""),
                "emotional_range": meta.get("emotional_range", ""),
                "body_language": meta.get("body_language", ""),
                "voice": meta.get("voice", ""),
                "status": meta.get("status", ""),
                "description": meta.get("description", ""),
                "prompt": meta.get("prompt", ""),
                "feedback": meta.get("feedback", []),
                "image": images[0] if images else None,
                "audio": audios[0] if audios else None,
                "images": images,
                "audios": audios,
            })
    return render_template("assets.html", scope_id=assets_scope, scope_title=scope_title, assets=assets, season=season)

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
    if field in ("name", "type", "role", "appearance", "personality", "distinguishing", "wardrobe", "emotional_range", "body_language", "voice", "status", "description", "prompt"):
        meta[field] = value
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
