from datetime import datetime
class GameHistory:
    def __init__(self): self.items=[]
    def record(self, room_id, game, winner=None): self.items.append({'room_id':room_id,'game':game,'winner':winner,'at':datetime.utcnow().isoformat()})
    def recent(self, limit=50): return self.items[-limit:]
