from .common import BaseGame,deck
from .teen_patti import _eval,TeenPatti
class PokerStyleGame(BaseGame):
    game_type="POKER_STYLE"; max_players=6
    def __init__(self,room_id):super().__init__(room_id);self.hands={};self.pot=0
    def start(self):
        if len(self.players)<2:return False
        d=deck();self.hands={p["user_id"]:[d.pop() for _ in range(5)] for p in self.players};self.status="SHOWDOWN";self.deadline(20);return True
    def showdown(self):
        best=None
        for p in self.players:
            h=self.hands[p["user_id"]]
            # compare by top 3 cards as a compact virtual-social demo ranking
            score=sorted((c["value"] for c in h),reverse=True)[:3]
            if best is None or score>best[0]:best=(score,p)
        self.status="FINISHED";self.winner=best[1]["user_id"];return self.state()
    def state(self):
        return {"game":self.game_type,"status":self.status,"players":[{**self.public_player(p),"hand":self.hands.get(p["user_id"],[]) if self.status=="FINISHED" else "HIDDEN"} for p in self.players],"winner":getattr(self,"winner",None)}
