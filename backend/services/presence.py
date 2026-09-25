import time
class Presence:
    def __init__(self): self.users={}
    def online(self, uid): self.users[str(uid)] = time.time()
    def offline(self, uid): self.users.pop(str(uid), None)
    def snapshot(self): return dict(self.users)
