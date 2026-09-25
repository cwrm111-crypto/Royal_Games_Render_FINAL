from .common import BaseGame, deck
class HazariGame(BaseGame):
    game_type="HAZARI"; max_players=4
    def __init__(self,room_id):
        super().__init__(room_id); self.hands={}; self.pot=0; self.packed=set()
    def start(self):
        if len(self.players)<2:return False
        d=deck(); self.hands={p["user_id"]:[d.pop() for _ in range(3)] for p in self.players}; self.pot=0;self.packed=set();self.turn=0;self.status="PLAYING";self.settled=False;self.winner_uid=None;self.deadline(15);return True
    def action(self,uid,a,wallet_debit):
        if self.status!="PLAYING" or uid!=self.players[self.turn]["user_id"]:return None
        if a=="PACK":self.packed.add(uid)
        elif a=="CALL":
            if wallet_debit(uid,10) is None:return {"error":"INSUFFICIENT_COINS"}
            self.pot+=10
        else:return {"error":"INVALID_ACTION"}
        active=[p for p in self.players if p["user_id"] not in self.packed]
        if len(active)<=1:
            self.status="FINISHED"
            self.winner_uid=active[0]["user_id"] if active else None
        else:self.turn=(self.turn+1)%len(self.players);self.deadline(15)
        return self.state()
    def state(self):
        return {"game":self.game_type,"status":self.status,"turn":self.turn,"deadline":self.turn_deadline,"pot":self.pot,
                "players":[{**self.public_player(p),"cards":self.hands.get(p["user_id"],[]) if self.status=="FINISHED" else "HIDDEN"} for p in self.players]}
