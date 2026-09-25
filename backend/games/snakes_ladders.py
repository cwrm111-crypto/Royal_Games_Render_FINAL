import random
from .common import BaseGame
class SnakesLaddersGame(BaseGame):
    game_type="SNAKES_LADDERS"; max_players=4
    JUMPS={3:22,5:8,11:26,20:29,27:1,36:6,47:26,58:18,70:55,76:45,78:59,87:24,91:73,97:78,99:80}
    def __init__(self,room_id):super().__init__(room_id);self.positions={};self.dice=None
    def start(self):
        if len(self.players)<2:return False
        self.status="PLAYING";self.turn=0;self.positions={p["user_id"]:0 for p in self.players};self.deadline(20);return True
    def roll(self,uid):
        if self.status!="PLAYING" or uid!=self.players[self.turn]["user_id"]:return None
        self.dice=random.SystemRandom().randint(1,6);p=self.positions[uid];target=p+self.dice
        if target<=100:self.positions[uid]=self.JUMPS.get(target,target)
        if self.positions[uid]==100:self.status="FINISHED";self.winner=uid
        elif self.dice!=6:self.turn=(self.turn+1)%len(self.players)
        self.deadline(20);return self.state()
    def state(self):return {"game":self.game_type,"status":self.status,"turn":self.turn,"dice":self.dice,"positions":self.positions,"players":self.public_players(),"deadline":self.turn_deadline}
