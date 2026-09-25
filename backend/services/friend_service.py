class FriendService:
    def __init__(self): self.links={}
    def add(self, a,b):
        self.links.setdefault(str(a),set()).add(str(b)); self.links.setdefault(str(b),set()).add(str(a))
    def friends(self, uid): return sorted(self.links.get(str(uid),set()))
