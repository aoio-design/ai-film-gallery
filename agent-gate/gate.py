#!/usr/bin/env python3
"""
AOIO agent login gate — email + password sign-in for the Hermes Web UI.

The Web UI upstream ships a single shared password. Rather than patching its
source (which would conflict on every update), this gate owns ONLY the login
surface and hands the browser the Web UI's own session cookie:

    browser  ->  GET  /login            -> this gate (AOIO email + password page)
    browser  ->  POST /api/auth/login   -> this gate: verify email+password in the
                                           AOIO account store, then relay to the
                                           Web UI's own /api/auth/login with the
                                           internal shared password and pass its
                                           Set-Cookie straight back
    browser  ->  everything else        -> the Web UI directly (untouched)

cloudflared routes only those two paths here (see ingress rules), so the Web UI's
password form is not reachable from the internet and its password becomes an
internal secret.

There is deliberately NO "forgot password" flow: this box runs no mail server,
so a reset link could never be delivered. Resets happen from the terminal:

    python3 /opt/data/aoio-auth/aoio_auth.py passwd you@example.com

Config (env):
    AGENT_GATE_PORT      listen port                (default 8790)
    AGENT_GATE_HOST      bind address               (default 0.0.0.0)
    WEBUI_URL            upstream Web UI            (default http://127.0.0.1:8787)
    WEBUI_ENV_FILE       .env holding the Web UI password
                                                    (default /opt/data/hermes-webui/.env)
    WEBUI_PASSWORD       overrides the .env lookup
    AOIO_AUTH_DIR        account store dir          (default /opt/data/aoio-auth)
    AGENT_GATE_TITLE     product name on the page   (default "Hermes")
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

def _find_account_store() -> str:
    """Locate aoio_auth.py: $AOIO_AUTH_DIR, ../accounts (public repo layout),
    then /opt/data/aoio-auth."""
    here = Path(__file__).resolve().parent
    for cand in (os.environ.get("AOIO_AUTH_DIR"), str(here.parent / "accounts"),
                 "/opt/data/aoio-auth"):
        if cand and (Path(cand) / "aoio_auth.py").is_file():
            return cand
    raise SystemExit("aoio_auth.py not found — set AOIO_AUTH_DIR to the folder holding it")


sys.path.insert(0, _find_account_store())
import aoio_auth  # noqa: E402

PORT = int(os.environ.get("AGENT_GATE_PORT", "8790"))
HOST = os.environ.get("AGENT_GATE_HOST", "0.0.0.0")
WEBUI_URL = os.environ.get("WEBUI_URL", "http://127.0.0.1:8787").rstrip("/")
WEBUI_ENV_FILE = Path(os.environ.get("WEBUI_ENV_FILE", "/opt/data/hermes-webui/.env"))
TITLE = os.environ.get("AGENT_GATE_TITLE", "Hermes")
ALLOWED_ROLES = ("owner",)          # the agent is owner-only; reviewers get the studio
RATE_LIMIT, RATE_WINDOW = 10, 300   # attempts per IP per 5 minutes
_attempts: dict[str, list[float]] = {}


# --- upstream password -----------------------------------------------------
def webui_password() -> str:
    """Resolve the Web UI's internal password: env var first, then its .env."""
    pw = os.environ.get("WEBUI_PASSWORD", "")
    if pw:
        return pw
    try:
        for line in WEBUI_ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("HERMES_WEBUI_PASSWORD="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


# --- helpers ---------------------------------------------------------------
def rate_ok(ip: str) -> bool:
    now = time.time()
    hits = [t for t in _attempts.get(ip, []) if now - t < RATE_WINDOW]
    _attempts[ip] = hits
    if len(_attempts) > 5000:          # bound memory against IP-spread floods
        _attempts.clear()
    return len(hits) < RATE_LIMIT


def rate_hit(ip: str) -> None:
    _attempts.setdefault(ip, []).append(time.time())


def safe_next(raw: str) -> str:
    """Only allow same-site path redirects; never bounce back to /login."""
    if not raw or not raw.startswith("/") or raw.startswith("//") or raw.startswith("/\\"):
        return "/"
    if re.search(r"[\x00-\x1f\x7f\s]", raw) or len(raw) > 512:
        return "/"
    if raw.split("?")[0].rstrip("/").endswith("/login"):
        return "/"
    return raw


LOGIN_PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — Sign in</title>
<style>
:root {
  --bg:#0a0c12; --bg2:#0e1119; --panel:#131722; --line:#242b3d;
  --text:#e8ebf2; --mut:#96a0b4; --gold:#c9a86a; --gold-dim:rgba(201,168,106,.12);
  --sans:system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',sans-serif;
  --serif:Georgia,'Times New Roman',serif;
}
html.light { --bg:#f4f3ef; --bg2:#fbfaf7; --panel:#fff; --line:#ded9cc;
  --text:#232a3a; --mut:#6b7280; --gold:#a67c2e; --gold-dim:rgba(166,124,46,.12); }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:var(--sans); background:var(--bg); color:var(--text);
  display:flex; align-items:center; justify-content:center; min-height:100vh; }
.box { background:var(--panel); border:1px solid var(--line); border-radius:12px;
  padding:40px; width:360px; }
h1 { font-family:var(--serif); font-size:22px; margin-bottom:6px; }
h1 span { color:var(--gold); }
p.sub { color:var(--mut); font-size:13px; margin-bottom:22px; }
input { width:100%; padding:12px; border-radius:6px; border:1px solid var(--line);
  background:var(--bg2); color:var(--text); font-size:16px; margin-bottom:14px;
  font-family:var(--sans); }
input:focus { outline:none; border-color:var(--gold); }
button { width:100%; padding:12px; border-radius:6px; border:1px solid var(--gold);
  background:var(--gold-dim); color:var(--gold); font-size:16px; cursor:pointer;
  font-family:var(--sans); }
button:hover { background:var(--gold); color:#0a0c12; }
button[disabled] { opacity:.5; cursor:default; }
#passkey { display:none; margin-top:10px; background:transparent; }
#err { color:#e05d6f; font-size:14px; margin-bottom:14px; display:none; }
.hint { color:var(--mut); font-size:12.5px; line-height:1.55; margin-top:18px;
  border-top:1px solid var(--line); padding-top:14px; }
#theme { position:fixed; top:14px; right:18px; cursor:pointer; font-size:17px;
  width:38px; height:38px; display:flex; align-items:center; justify-content:center;
  background:var(--panel); border:1px solid var(--line); border-radius:50%; user-select:none; }
</style></head><body>
<div id="theme" title="Toggle light / dark">🌙</div>
<div class="box">
  <h1>__TITLE__ <span>Agent</span></h1>
  <p class="sub">Sign in with your email and password.</p>
  <div id="err"></div>
  <form id="f">
    <input id="email" type="email" placeholder="Email" autocomplete="username" spellcheck="false" autofocus>
    <input id="pw" type="password" placeholder="Password" autocomplete="current-password">
    <button type="submit" id="go">Sign in</button>
  </form>
  <button id="passkey" type="button">Sign in with passkey</button>
  <div class="hint">Forgot your password? This server can't email you — it runs no
    mail server. Ask your Hermes agent to reset it from the terminal.</div>
</div>
<script>
(function(){
  var t=localStorage.getItem('aio-theme');
  if(t==='light'){document.documentElement.classList.add('light');
    document.getElementById('theme').textContent='☀️';}
  document.getElementById('theme').addEventListener('click',function(){
    var h=document.documentElement; h.classList.toggle('light');
    var l=h.classList.contains('light');
    localStorage.setItem('aio-theme', l?'light':'dark');
    this.textContent = l?'☀️':'🌙';
  });
  var f=document.getElementById('f'), err=document.getElementById('err'),
      go=document.getElementById('go'), pk=document.getElementById('passkey');
  function showErr(m){ err.textContent=m; err.style.display='block'; }
  function nextPath(){
    try{
      var raw=new URL(window.location.href).searchParams.get('next');
      if(!raw||raw.charAt(0)!=='/'||raw.charAt(1)==='/') return '/';
      if(/\\/login\\/?$/.test(raw.split('?')[0])) return '/';
      return raw;
    }catch(e){ return '/'; }
  }
  f.addEventListener('submit', async function(e){
    e.preventDefault(); err.style.display='none'; go.disabled=true;
    try{
      var res=await fetch('/api/auth/login',{method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({email:document.getElementById('email').value,
                             password:document.getElementById('pw').value}),
        credentials:'include'});
      var data={}; try{ data=await res.json(); }catch(_){}
      if(res.ok&&data.ok){ window.location.href=nextPath(); return; }
      showErr(data.error||'Wrong email or password');
    }catch(ex){ showErr('Connection failed — is the agent running?'); }
    go.disabled=false;
  });
  // Passkeys stay handled by the Web UI itself (these paths are not gated).
  function b64u(s){ s=String(s||'').replace(/-/g,'+').replace(/_/g,'/');
    while(s.length%4) s+='='; var b=atob(s), o=new Uint8Array(b.length);
    for(var i=0;i<b.length;i++) o[i]=b.charCodeAt(i); return o; }
  function toB64u(buf){ var b=new Uint8Array(buf), s='';
    for(var i=0;i<b.length;i++) s+=String.fromCharCode(b[i]);
    return btoa(s).replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,''); }
  if(window.PublicKeyCredential&&navigator.credentials){
    fetch('/api/auth/status',{credentials:'include'})
      .then(function(r){ return r.ok?r.json():null; })
      .then(function(s){ if(s&&s.passkeys_enabled&&(s.passkeys||[]).length)
        pk.style.display='block'; }).catch(function(){});
    pk.addEventListener('click', async function(){
      err.style.display='none'; pk.disabled=true;
      try{
        var o=await fetch('/api/auth/passkey/options',{method:'POST',body:'{}',credentials:'include'});
        var od=await o.json();
        if(!o.ok||!od.publicKey) throw new Error(od.error||'Passkey unavailable');
        var p=od.publicKey; p.challenge=b64u(p.challenge);
        if(Array.isArray(p.allowCredentials))
          p.allowCredentials=p.allowCredentials.map(function(c){
            return Object.assign({},c,{id:b64u(c.id)}); });
        var cred=await navigator.credentials.get({publicKey:p});
        var payload={id:cred.id,rawId:toB64u(cred.rawId),type:cred.type,response:{
          authenticatorData:toB64u(cred.response.authenticatorData),
          clientDataJSON:toB64u(cred.response.clientDataJSON),
          signature:toB64u(cred.response.signature),
          userHandle:cred.response.userHandle?toB64u(cred.response.userHandle):null}};
        var r=await fetch('/api/auth/passkey/login',{method:'POST',
          headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),
          credentials:'include'});
        var d={}; try{ d=await r.json(); }catch(_){}
        if(r.ok&&d.ok){ window.location.href=nextPath(); return; }
        showErr(d.error||'Passkey sign-in failed');
      }catch(ex){ showErr(ex&&ex.message?ex.message:'Passkey sign-in failed'); }
      pk.disabled=false;
    });
  }
})();
</script></body></html>
"""


# --- upstream relay --------------------------------------------------------
def webui_login_cookies() -> tuple[bool, list[str], str]:
    """Log in to the Web UI with the internal password.

    Returns (ok, set_cookie_headers, error_message).
    """
    pw = webui_password()
    if not pw:
        return False, [], "Web UI password not configured on the server"
    req = urllib.request.Request(
        WEBUI_URL + "/api/auth/login",
        data=json.dumps({"password": pw}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "AOIO-agent-gate/1.0"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            body = json.loads(r.read().decode() or "{}")
            cookies = r.headers.get_all("Set-Cookie") or []
            if body.get("ok") and cookies:
                return True, list(cookies), ""
            if body.get("ok"):
                # Auth disabled upstream: nothing to hand back, but not a failure.
                return True, [], ""
            return False, [], "Agent rejected the internal login"
    except urllib.error.HTTPError:
        return False, [], "Agent rejected the internal login (check HERMES_WEBUI_PASSWORD)"
    except Exception:
        return False, [], "Agent is not reachable"


def webui_logged_in(cookie_header: str) -> bool:
    if not cookie_header:
        return False
    req = urllib.request.Request(
        WEBUI_URL + "/api/auth/status",
        headers={"Cookie": cookie_header, "User-Agent": "AOIO-agent-gate/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return bool(json.loads(r.read().decode() or "{}").get("logged_in"))
    except Exception:
        return False


class Gate(BaseHTTPRequestHandler):
    server_version = "AOIO-agent-gate"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # quieter, and never logs bodies
        sys.stderr.write("%s %s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"),
                                         self.client_ip(), fmt % args))

    # --- utils ---
    def client_ip(self) -> str:
        """Caller IP for throttling. Only CF-Connecting-IP is trusted (Cloudflare
        sets it and strips any client-supplied copy); X-Forwarded-For is NOT, since
        any client can send it and use it to spread brute-force attempts across
        fake IPs. Falls back to the socket address."""
        cf = (self.headers.get("CF-Connecting-IP") or "").strip()
        return cf.split(",")[0].strip() if cf else self.client_address[0]

    def is_https(self) -> bool:
        return self.headers.get("X-Forwarded-Proto", "").lower() == "https"

    def _head(self, status: int, ctype: str, length: int, cookies: list[str] | None = None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        for c in cookies or []:
            if self.is_https() and "secure" not in c.lower():
                c += "; Secure"
            self.send_header("Set-Cookie", c)
        self.end_headers()

    def send_html(self, html: str, status: int = 200):
        body = html.encode()
        self._head(status, "text/html; charset=utf-8", len(body))
        self.wfile.write(body)

    def send_json(self, obj: dict, status: int = 200, cookies: list[str] | None = None):
        body = json.dumps(obj).encode()
        self._head(status, "application/json", len(body), cookies)
        self.wfile.write(body)

    def redirect(self, to: str, cookies: list[str] | None = None):
        self.send_response(302)
        self.send_header("Location", to)
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        for c in cookies or []:
            if self.is_https() and "secure" not in c.lower():
                c += "; Secure"
            self.send_header("Set-Cookie", c)
        self.end_headers()

    # --- routes ---
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            body = b"ok"
            self._head(200, "text/plain", len(body))
            self.wfile.write(body)
            return
        if path == "/login":
            # Already signed in? Go straight through.
            if webui_logged_in(self.headers.get("Cookie", "")):
                q = parse_qs(urlparse(self.path).query)
                return self.redirect(safe_next((q.get("next") or ["/"])[0]))
            return self.send_html(LOGIN_PAGE.replace("__TITLE__", TITLE))
        self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/auth/login":
            return self.send_json({"error": "not found"}, 404)

        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(min(length, 8192)) if length else b""
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip()
        if ctype == "application/json":
            try:
                data = json.loads(raw.decode() or "{}")
            except Exception:
                data = {}
            form_post = False
        else:
            q = parse_qs(raw.decode(errors="replace"))
            data = {k: v[0] for k, v in q.items()}
            form_post = True

        email = str(data.get("email") or "").strip().lower()
        password = str(data.get("password") or "")
        ip = self.client_ip()

        if not rate_ok(ip):
            self.log_message("login rate-limited (%s)", email or "-")
            return self.send_json({"error": "Too many attempts. Try again in a few minutes."}, 429)

        user = aoio_auth.verify(email, password, roles=ALLOWED_ROLES)
        if not user:
            rate_hit(ip)
            self.log_message("login REJECTED (%s)", email or "-")
            return self.send_json({"error": "Wrong email or password"}, 401)

        ok, cookies, err = webui_login_cookies()
        if not ok:
            self.log_message("upstream login FAILED for %s: %s", email, err)
            return self.send_json({"error": err}, 502)

        self.log_message("login ok (%s)", email)
        if form_post:
            return self.redirect("/", cookies)
        return self.send_json({"ok": True, "email": user["email"]}, 200, cookies)


def main() -> int:
    if not webui_password():
        print(f"[warn] no Web UI password found (checked $WEBUI_PASSWORD and {WEBUI_ENV_FILE}); "
              f"logins will fail until it is set", flush=True)
    if aoio_auth.count_users() == 0:
        print("[warn] no accounts in the AOIO account store — create one with: "
              "python3 /opt/data/aoio-auth/aoio_auth.py add you@example.com", flush=True)
    print(f"AOIO agent gate on http://{HOST}:{PORT} -> {WEBUI_URL} "
          f"(accounts: {aoio_auth.count_users()})", flush=True)
    ThreadingHTTPServer((HOST, PORT), Gate).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
