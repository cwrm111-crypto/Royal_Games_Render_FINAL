import os, sqlite3, threading
from datetime import datetime

DB_PATH = os.getenv("DATABASE_PATH", "data/royal_games.sqlite3")
_lock = threading.RLock()

def _conn():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with _lock, _conn() as c:
        c.executescript("""
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS users(
          id TEXT PRIMARY KEY, name TEXT NOT NULL, username TEXT, coins INTEGER NOT NULL DEFAULT 5000,
          xp INTEGER NOT NULL DEFAULT 0, level INTEGER NOT NULL DEFAULT 1, wins INTEGER NOT NULL DEFAULT 0,
          losses INTEGER NOT NULL DEFAULT 0, banned INTEGER NOT NULL DEFAULT 0, last_daily TEXT, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS transactions(
          id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, amount INTEGER NOT NULL,
          type TEXT NOT NULL, note TEXT, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS rooms(
          room_id TEXT PRIMARY KEY, game_type TEXT NOT NULL, status TEXT NOT NULL,
          snapshot TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS friends(
          user_id TEXT NOT NULL, friend_id TEXT NOT NULL, created_at TEXT NOT NULL,
          PRIMARY KEY(user_id, friend_id)
        );
        CREATE TABLE IF NOT EXISTS tournaments(
          id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, game_type TEXT NOT NULL,
          entry_fee INTEGER NOT NULL, prize_pool INTEGER NOT NULL, max_players INTEGER NOT NULL,
          status TEXT NOT NULL DEFAULT 'UPCOMING', starts_at TEXT NOT NULL
        );
        """)
        c.commit()

def get_user(user_id):
    with _lock, _conn() as c:
        r=c.execute("SELECT * FROM users WHERE id=?", (str(user_id),)).fetchone()
        return dict(r) if r else None

def ensure_user(user_id, name="Player", username=None, start_coins=5000):
    uid=str(user_id)
    with _lock, _conn() as c:
        r=c.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
        if r: return dict(r)
        now=datetime.utcnow().isoformat()
        c.execute("INSERT INTO users(id,name,username,coins,created_at) VALUES(?,?,?,?,?)",(uid,name,username,start_coins,now))
        c.execute("INSERT INTO transactions(user_id,amount,type,note,created_at) VALUES(?,?,?,?,?)",(uid,start_coins,"WELCOME","Starting virtual coins",now))
        c.commit()
        return get_user(uid)

def update_user(user_id, **fields):
    allowed={"name","username","coins","xp","level","wins","losses","banned","last_daily"}
    fields={k:v for k,v in fields.items() if k in allowed}
    if not fields:return get_user(user_id)
    with _lock,_conn() as c:
        sets=", ".join(f"{k}=?" for k in fields)
        vals=list(fields.values())+[str(user_id)]
        c.execute(f"UPDATE users SET {sets} WHERE id=?", vals); c.commit()
    return get_user(user_id)

def tx(user_id, amount, tx_type, note=""):
    now=datetime.utcnow().isoformat()
    with _lock,_conn() as c:
        c.execute("INSERT INTO transactions(user_id,amount,type,note,created_at) VALUES(?,?,?,?,?)",(str(user_id),amount,tx_type,note,now))
        c.commit()

def adjust_coins(user_id, delta, tx_type, note=""):
    with _lock,_conn() as c:
        r=c.execute("SELECT coins FROM users WHERE id=?", (str(user_id),)).fetchone()
        if not r: return None
        new=max(0,int(r["coins"])+int(delta))
        c.execute("UPDATE users SET coins=? WHERE id=?", (new,str(user_id)))
        now=datetime.utcnow().isoformat()
        c.execute("INSERT INTO transactions(user_id,amount,type,note,created_at) VALUES(?,?,?,?,?)",(str(user_id),int(delta),tx_type,note,now))
        c.commit()
        return new

def transactions(user_id, limit=50):
    with _lock,_conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY id DESC LIMIT ?",(str(user_id),int(limit))).fetchall()]

def leaderboard(limit=100):
    with _lock,_conn() as c:
        return [dict(r) for r in c.execute("SELECT id,name,coins,xp,level,wins,losses FROM users WHERE banned=0 ORDER BY coins DESC LIMIT ?",(int(limit),)).fetchall()]

def set_room(room_id, game_type, status, snapshot):
    import json
    with _lock,_conn() as c:
        c.execute("""INSERT INTO rooms(room_id,game_type,status,snapshot,updated_at) VALUES(?,?,?,?,?)
        ON CONFLICT(room_id) DO UPDATE SET status=excluded.status,snapshot=excluded.snapshot,updated_at=excluded.updated_at""",
        (room_id,game_type,status,json.dumps(snapshot,ensure_ascii=False),datetime.utcnow().isoformat())); c.commit()

def room_rows():
    with _lock,_conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM rooms ORDER BY updated_at DESC").fetchall()]
