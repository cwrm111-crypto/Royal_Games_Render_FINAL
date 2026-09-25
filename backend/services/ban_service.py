class BanService:
    def __init__(self): self.banned=set()
    def ban(self, uid): self.banned.add(str(uid))
    def unban(self, uid): self.banned.discard(str(uid))
    def is_banned(self, uid): return str(uid) in self.banned
