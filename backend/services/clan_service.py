class ClanService:
    def __init__(self): self.clans={}
    def create(self, cid, owner): self.clans[cid]={'owner':owner,'members':{str(owner)}}; return self.clans[cid]
    def join(self, cid, uid): self.clans[cid]['members'].add(str(uid))
