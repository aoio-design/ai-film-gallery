#!/usr/bin/env python3
"""Gallery feedback watcher — SILENT when nothing new; prints a digest of new feedback.

Scans every shot's metadata.json feedback[] plus each project's _episode_script.json
feedback[] under the gallery's shots/ dir. Only reports entries newer than the last
run (marker file), with a 60s grace period so in-flight saves aren't double-reported.
First run records the baseline silently (no spam of historical feedback).

Wire it up: hermes cron create 'every 30m' --name 'Gallery feedback watcher' --no-agent --script gallery-feedback-watch.py
"""
import json
import os
from datetime import datetime, timezone

GALLERY = os.environ.get("GALLERY_DIR", "/opt/data/gallery")
STATE = os.path.join(GALLERY, ".feedback-watch-state")


def parse_ts(s):
    try:
        return datetime.fromisoformat(s).timestamp()
    except Exception:
        return 0.0


def main():
    last = 0.0
    first_run = not os.path.exists(STATE)
    if not first_run:
        try:
            last = float(open(STATE).read().strip())
        except Exception:
            last = 0.0

    found = []
    shots_root = os.path.join(GALLERY, "shots")
    if os.path.isdir(shots_root):
        for root, _dirs, files in os.walk(shots_root):
            for fn in files:
                if fn not in ("metadata.json", "_episode_script.json"):
                    continue
                try:
                    with open(os.path.join(root, fn)) as f:
                        data = json.load(f)
                except Exception:
                    continue
                for fb in data.get("feedback", []):
                    t = parse_ts(fb.get("timestamp", ""))
                    if t > last + 60:
                        loc = os.path.relpath(root, GALLERY)
                        found.append((fb.get("timestamp", "")[:16], loc, fb.get("text", "")[:90]))

    with open(STATE, "w") as f:
        f.write(str(datetime.now(timezone.utc).timestamp()))

    if first_run or not found:
        return  # silent

    print(f"🎬 New gallery feedback ({len(found)}):")
    for ts_str, loc, txt in found:
        print(f"  {ts_str} · {loc}: {txt}")
    print("Process it: read the feedback files and regenerate/revise accordingly.")


if __name__ == "__main__":
    main()
