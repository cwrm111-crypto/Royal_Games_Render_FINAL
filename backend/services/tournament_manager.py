class TournamentManager:
    def __init__(self): self.items={}
    def create(self, tid, game, entry=0, prize=0): self.items[tid]={'game':game,'entry':entry,'prize':prize,'players':[]}; return self.items[tid]
    def join(self, tid, uid):
        self.items[tid]['players'].append(str(uid)); return self.items[tid]
