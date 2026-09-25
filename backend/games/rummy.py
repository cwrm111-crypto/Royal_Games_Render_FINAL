from .common import BaseGame, deck
class RummyGame(BaseGame):
    game_type="RUMMY"; max_players=6
    def __init__(self,room_id):
        super().__init__(room_id); self.deck=[]; self.discard=[]; self.hands={}; self.drawn=set()
    def start(self):
        if len(self.players)<2:return False
        self.deck=deck(); self.discard=[self.deck.pop()]; self.hands={p["user_id"]:[self.deck.pop() for _ in range(13)] for p in self.players}
        self.turn=0; self.status="PLAYING"; self.deadline(30); return True
    def draw(self,uid,source="DECK"):
        if self.status!="PLAYING" or self.players[self.turn]["user_id"]!=uid:return None
        card=self.discard.pop() if source=="DISCARD" and self.discard else self.deck.pop()
        self.hands[uid].append(card); self.drawn.add(uid); self.deadline(30); return self.state(uid)
    def discard_card(self,uid,index):
        if self.status!="PLAYING" or self.players[self.turn]["user_id"]!=uid or uid not in self.drawn:return None
        hand=self.hands[uid]
        if index<0 or index>=len(hand):return None
        self.discard.append(hand.pop(index)); self.drawn.discard(uid); self.turn=(self.turn+1)%len(self.players); self.deadline(30)
        return self.state(uid)
    def declare(self,uid):
        if len(self.hands.get(uid,[]))==13:
            self.status="FINISHED"; self.winner=uid
            return self.state(uid)
        return {"error":"DECLARE_REQUIRES_13_CARDS"}
    def timeout(self):
        if self.status=="PLAYING":
            uid=self.players[self.turn]["user_id"]
            if uid in self.drawn and self.hands[uid]: self.discard_card(uid,len(self.hands[uid])-1)
            else:self.turn=(self.turn+1)%len(self.players);self.deadline(30)
            return self.state(None)
    def state(self,viewer=None):
        ps=[]
        for p in self.players:
            uid=p["user_id"]; x=self.public_player(p); x["hand_count"]=len(self.hands.get(uid,[])); x["hand"]=self.hands.get(uid,[]) if uid==viewer or self.status=="FINISHED" else "HIDDEN"; ps.append(x)
        return {"game":self.game_type,"status":self.status,"turn":self.turn,"deadline":self.turn_deadline,"discard":self.discard[-1:] ,"players":ps}
