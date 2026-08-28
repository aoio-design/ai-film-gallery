#!/usr/bin/env python3
"""
AOIO account store — one email + password login shared by every private
surface on this box (studio gallery, agent Web UI gate).

Stdlib only (sqlite3 + hashlib.scrypt) so any app can import it regardless of
which virtualenv it runs in:

    import sys; sys.path.insert(0, "/opt/data/aoio-auth")
    import aoio_auth
    user = aoio_auth.verify(email, password, roles=("owner",))

There is deliberately NO password-reset-by-email flow: this box does not run a
mail server, so a "forgot password" link could never deliver anything. Password
resets are done from the terminal (or by asking the agent):

    python3 /opt/data/aoio-auth/aoio_auth.py passwd you@example.com

Storage: users.db (sqlite, chmod 600) next to this file, or $AOIO_AUTH_DB.
Hashes: scrypt (n=2**15, r=8, p=1), 16-byte salt, stored as
        scrypt$n$r$p$<salt_b64>$<hash_b64>
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import sqlite3
import sys
import time
from pathlib import Path

# --- config ---------------------------------------------------------------
DB_PATH = Path(os.environ.get("AOIO_AUTH_DB") or (Path(__file__).resolve().parent / "users.db"))

ROLES = ("owner", "reviewer")          # owner = studio + agent, reviewer = studio only
_SCRYPT_N, _SCRYPT_R, _SCRYPT_P = 2 ** 15, 8, 1
_DUMMY_HASH = None                     # lazily built, used for constant-work misses
MIN_PASSWORD_LEN = 12          # public source: strength must come from the password


# --- hashing --------------------------------------------------------------
def hash_password(password: str, *, salt: bytes | None = None) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")
    salt = salt or secrets.token_bytes(16)
    dk = hashlib.scrypt(password.encode("utf-8"), salt=salt,
                        n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P, dklen=32,
                        maxmem=64 * 1024 * 1024)
    b64 = lambda b: base64.b64encode(b).decode()
    return f"scrypt${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${b64(salt)}${b64(dk)}"


def _check_hash(stored: str, password: str) -> bool:
    """Constant-time verify against a stored hash string. False on any garbage."""
    try:
        algo, n, r, p, salt_b64, hash_b64 = stored.split("$")
        if algo != "scrypt":
            return False
        dk = hashlib.scrypt(password.encode("utf-8"),
                            salt=base64.b64decode(salt_b64),
                            n=int(n), r=int(r), p=int(p),
                            dklen=len(base64.b64decode(hash_b64)),
                            maxmem=64 * 1024 * 1024)
        return hmac.compare_digest(dk, base64.b64decode(hash_b64))
    except Exception:
        return False


def _burn_cycles(password: str) -> None:
    """Spend the same work on a missing/disabled user so response time does not
    leak whether the address exists."""
    global _DUMMY_HASH
    if _DUMMY_HASH is None:
        _DUMMY_HASH = hash_password("aoio-nonexistent-user-placeholder")
    _check_hash(_DUMMY_HASH, password)


# --- db -------------------------------------------------------------------
def _db() -> sqlite3.Connection:
    first = not DB_PATH.exists()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        email       TEXT PRIMARY KEY,
        name        TEXT DEFAULT '',
        pw_hash     TEXT NOT NULL,
        role        TEXT NOT NULL DEFAULT 'owner',
        created_at  INTEGER NOT NULL,
        updated_at  INTEGER NOT NULL,
        disabled    INTEGER NOT NULL DEFAULT 0,
        last_login  INTEGER
    )""")
    conn.commit()
    if first:
        try:
            os.chmod(DB_PATH, 0o600)
        except OSError:
            pass
    return conn


def norm_email(email: str) -> str:
    return (email or "").strip().lower()


def _row_to_user(row: sqlite3.Row) -> dict:
    return {"email": row["email"], "name": row["name"] or "", "role": row["role"],
            "disabled": bool(row["disabled"]), "created_at": row["created_at"],
            "last_login": row["last_login"]}


# --- public API -----------------------------------------------------------
def count_users() -> int:
    with _db() as conn:
        return int(conn.execute("SELECT COUNT(*) FROM users").fetchone()[0])


def get_user(email: str) -> dict | None:
    with _db() as conn:
        row = conn.execute("SELECT * FROM users WHERE email=?", (norm_email(email),)).fetchone()
    return _row_to_user(row) if row else None


def list_users() -> list[dict]:
    with _db() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY created_at").fetchall()
    return [_row_to_user(r) for r in rows]


def add_user(email: str, password: str, name: str = "", role: str = "owner",
             *, replace: bool = False) -> dict:
    email = norm_email(email)
    if "@" not in email or len(email) < 5:
        raise ValueError(f"not a valid email address: {email!r}")
    if role not in ROLES:
        raise ValueError(f"role must be one of {ROLES}")
    if len(password or "") < MIN_PASSWORD_LEN:
        raise ValueError(f"password must be at least {MIN_PASSWORD_LEN} characters")
    now = int(time.time())
    pw_hash = hash_password(password)
    with _db() as conn:
        if replace:
            conn.execute("""INSERT INTO users (email,name,pw_hash,role,created_at,updated_at)
                            VALUES (?,?,?,?,?,?)
                            ON CONFLICT(email) DO UPDATE SET
                              name=excluded.name, pw_hash=excluded.pw_hash,
                              role=excluded.role, updated_at=excluded.updated_at,
                              disabled=0""",
                         (email, name, pw_hash, role, now, now))
        else:
            if conn.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
                raise ValueError(f"user already exists: {email} (use passwd, or replace=True)")
            conn.execute("""INSERT INTO users (email,name,pw_hash,role,created_at,updated_at)
                            VALUES (?,?,?,?,?,?)""",
                         (email, name, pw_hash, role, now, now))
        conn.commit()
    return get_user(email)


def set_password(email: str, password: str) -> bool:
    if len(password or "") < MIN_PASSWORD_LEN:
        raise ValueError(f"password must be at least {MIN_PASSWORD_LEN} characters")
    with _db() as conn:
        cur = conn.execute("UPDATE users SET pw_hash=?, updated_at=? WHERE email=?",
                           (hash_password(password), int(time.time()), norm_email(email)))
        conn.commit()
        return cur.rowcount > 0


def set_disabled(email: str, disabled: bool = True) -> bool:
    with _db() as conn:
        cur = conn.execute("UPDATE users SET disabled=?, updated_at=? WHERE email=?",
                           (1 if disabled else 0, int(time.time()), norm_email(email)))
        conn.commit()
        return cur.rowcount > 0


def delete_user(email: str) -> bool:
    with _db() as conn:
        cur = conn.execute("DELETE FROM users WHERE email=?", (norm_email(email),))
        conn.commit()
        return cur.rowcount > 0


def verify(email: str, password: str, roles: tuple[str, ...] | None = None) -> dict | None:
    """Verify credentials. Returns the user dict on success, None otherwise.

    ``roles`` optionally restricts which roles may sign in to the calling
    surface (e.g. the agent Web UI gate passes roles=("owner",)). Fails closed:
    unknown address, disabled account, wrong role and bad password all return
    None after spending comparable work.
    """
    email = norm_email(email)
    if not email or not password:
        _burn_cycles(password or "")
        return None
    with _db() as conn:
        row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not row or row["disabled"]:
        _burn_cycles(password)
        return None
    if not _check_hash(row["pw_hash"], password):
        return None
    if roles is not None and row["role"] not in roles:
        return None
    with _db() as conn:
        conn.execute("UPDATE users SET last_login=? WHERE email=?", (int(time.time()), email))
        conn.commit()
    return _row_to_user(row)


def gen_password(words: int = 4) -> str:
    """Readable-but-strong password: 3 random chunks + digits."""
    alphabet = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    chunks = ["".join(secrets.choice(alphabet) for _ in range(5)) for _ in range(words - 1)]
    return "-".join(chunks) + "-" + str(secrets.randbelow(9000) + 1000)


# --- CLI ------------------------------------------------------------------
_USAGE = """AOIO accounts — email + password logins for studio / agent

  list                                  show accounts
  add <email> [password] [--name N] [--role owner|reviewer] [--replace]
  passwd <email> [password]             set a new password (generated if omitted)
  disable <email> | enable <email>
  delete <email>
  verify <email> <password>             test a login

Password is generated and printed when omitted. DB: %s
""" % DB_PATH


def _cli(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(_USAGE)
        return 0
    cmd, args = argv[0], argv[1:]
    flags = {a for a in args if a.startswith("--")}
    named = {}
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--name", "--role"):
            named[a[2:]] = args[i + 1] if i + 1 < len(args) else ""
            i += 2
            continue
        if not a.startswith("--"):
            rest.append(a)
        i += 1

    try:
        if cmd == "list":
            users = list_users()
            if not users:
                print("(no accounts yet)")
                return 0
            print(f"{'EMAIL':38} {'ROLE':9} {'STATE':9} LAST LOGIN")
            for u in users:
                last = (time.strftime("%Y-%m-%d %H:%M", time.localtime(u["last_login"]))
                        if u["last_login"] else "never")
                print(f"{u['email']:38} {u['role']:9} "
                      f"{'disabled' if u['disabled'] else 'active':9} {last}")
            return 0

        if cmd == "add":
            if not rest:
                print("usage: add <email> [password] [--name N] [--role owner|reviewer]")
                return 2
            email = rest[0]
            pw = rest[1] if len(rest) > 1 else gen_password()
            generated = len(rest) < 2
            u = add_user(email, pw, name=named.get("name", ""),
                         role=named.get("role", "owner"), replace="--replace" in flags)
            print(f"created {u['email']} (role {u['role']})")
            if generated:
                print(f"password: {pw}")
            return 0

        if cmd == "passwd":
            if not rest:
                print("usage: passwd <email> [password]")
                return 2
            email = rest[0]
            pw = rest[1] if len(rest) > 1 else gen_password()
            generated = len(rest) < 2
            if not set_password(email, pw):
                print(f"no such account: {email}")
                return 1
            print(f"password updated for {norm_email(email)}")
            if generated:
                print(f"password: {pw}")
            return 0

        if cmd in ("disable", "enable"):
            if not rest:
                print(f"usage: {cmd} <email>")
                return 2
            ok = set_disabled(rest[0], cmd == "disable")
            print(f"{'ok' if ok else 'no such account'}: {norm_email(rest[0])}")
            return 0 if ok else 1

        if cmd == "delete":
            if not rest:
                print("usage: delete <email>")
                return 2
            ok = delete_user(rest[0])
            print(f"{'deleted' if ok else 'no such account'}: {norm_email(rest[0])}")
            return 0 if ok else 1

        if cmd == "verify":
            # Password may come from $AOIO_PASSWORD instead of argv, so it does not
            # land in shell history or `ps` output.
            pw = rest[1] if len(rest) > 1 else os.environ.get("AOIO_PASSWORD", "")
            if not rest or not pw:
                print("usage: verify <email> <password>   (or set AOIO_PASSWORD)")
                return 2
            u = verify(rest[0], pw)
            print("OK: " + repr(u) if u else "REJECTED")
            return 0 if u else 1

    except ValueError as e:
        print(f"error: {e}")
        return 2

    print(f"unknown command: {cmd}\n\n{_USAGE}")
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
