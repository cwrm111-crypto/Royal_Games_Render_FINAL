import random
from .common import BaseGame
class LudoGame(BaseGame):
    game_type="LUDO"; max_players=4
    def __init__(self,room_id):super().__init__(room_id);self.tokens={};self.positions={};self.dice=None
    def start(self):
        if len(self.players)<2:return False
        self.status="PLAYING";self.turn=0;self.tokens={p["user_id"]:[0,0,0,0] for p in self.players};self.deadline(20);return True
    def roll(self,uid):
        if self.status!="PLAYING" or uid!=self.players[self.turn]["user_id"]:return None
        self.dice=random.SystemRandom().randint(1,6);self.deadline(20);return self.state(uid)
    def move(self,uid,token):
        if self.dice is None or uid!=self.players[self.turn]["user_id"] or token not in range(4):return None
        pos=self.tokens[uid][token]
        if pos==0 and self.dice!=6:return self.state(uid)
        self.tokens[uid][token]=min(57 if pos else 1,pos+self.dice)
        extra=self.dice==6
        self.dice=None
        if not extra:self.turn=(self.turn+1)%len(self.players)
        self.deadline(20);return self.state(uid)
    def state(self,viewer=None):
        return {"game":self.game_type,"status":self.status,"turn":self.turn,"dice":self.dice,"tokens":self.tokens,"players":self.public_players(),"deadline":self.turn_deadline}
