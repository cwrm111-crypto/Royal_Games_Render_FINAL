from backend import db
class FriendsService:
    def add(self,user_id,friend_id):
        with db._lock, db._conn() as c:
            c.execute("INSERT OR IGNORE INTO friends(user_id,friend_id,created_at) VALUES(?,?,datetime('now'))",(str(user_id),str(friend_id)))
            c.execute("INSERT OR IGNORE INTO friends(user_id,friend_id,created_at) VALUES(?,?,datetime('now'))",(str(friend_id),str(user_id)))
            c.commit()
        return {"success":True}
    def list(self,user_id):
        with db._lock, db._conn() as c:
            return [dict(r) for r in c.execute("SELECT u.id,u.name,u.username,u.coins FROM users u JOIN friends f ON f.friend_id=u.id WHERE f.user_id=?",(str(user_id),)).fetchall()]
