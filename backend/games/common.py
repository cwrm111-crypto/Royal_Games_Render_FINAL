import random, time
SUITS=["♠","♥","♦","♣"]
RANKS=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
VALUES={r:i+2 for i,r in enumerate(RANKS)}

def deck():
    cards=[{"suit":s,"rank":r,"value":VALUES[r]} for s in SUITS for r in RANKS]
    random.SystemRandom().shuffle(cards)
    return cards

class BaseGame:
    game_type="BASE"; max_players=6
    def __init__(self,room_id):
        self.room_id=room_id; self.players=[]; self.status="WAITING"; self.turn=0; self.turn_deadline=0; self.settled=False
    def add_player(self,p):
        if any(x["user_id"]==p["user_id"] for x in self.players): return True
        if self.status!="WAITING" or len(self.players)>=self.max_players: return False
        self.players.append(dict(p)); return True
    def public_player(self,p):
        out=dict(p)
        out.pop("sid",None)
        out.pop("cards",None)
        out.pop("hand",None)
        return out
    def public_players(self):
        return [self.public_player(p) for p in self.players]
    def deadline(self,seconds):
        self.turn_deadline=time.time()+seconds
