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
    return render_template("project_list.html", projects=data["projects"])

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

    return render_template("gallery.html", project=project)

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

if __name__ == "__main__":
    port = int(os.environ.get("GALLERY_PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
