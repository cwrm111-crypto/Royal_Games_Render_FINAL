from .common import BaseGame, deck
class CallBreakGame(BaseGame):
    game_type="CALL_BREAK"; max_players=4
    def __init__(self,room_id):
        super().__init__(room_id); self.hands={}; self.bids={}; self.trick=[]; self.tricks={}; self.trump="♠"; self.leader=0
    def start(self):
        if len(self.players)!=4:return False
        d=deck(); self.hands={p["user_id"]:[d.pop() for _ in range(13)] for p in self.players}; self.bids={}; self.tricks={p["user_id"]:0 for p in self.players}; self.trick=[]; self.turn=0; self.leader=0; self.status="BIDDING"; self.deadline(20); return True
    def bid(self,uid,b):
        if self.status!="BIDDING" or uid!=self.players[self.turn]["user_id"] or b<1 or b>13:return None
        self.bids[uid]=int(b); self.turn=(self.turn+1)%4
        if len(self.bids)==4:self.status="PLAYING";self.turn=self.leader;self.deadline(20)
        else:self.deadline(20)
        return self.state(uid)
    def play_card(self,uid,index):
        if self.status!="PLAYING" or uid!=self.players[self.turn]["user_id"]:return None
        hand=self.hands[uid]; 
        if index<0 or index>=len(hand):return None
        card=hand[index]; lead=self.trick[0]["card"]["suit"] if self.trick else None
        if lead and not any(c["suit"]==lead for c in hand) and card["suit"]!=self.trump:
            pass
        elif lead and any(c["suit"]==lead for c in hand) and card["suit"]!=lead:
            return {"error":"MUST_FOLLOW_SUIT"}
        hand.pop(index); self.trick.append({"uid":uid,"card":card})
        if len(self.trick)==4:
            lead_suit=self.trick[0]["card"]["suit"]
            winner=max(self.trick,key=lambda x:(x["card"]["suit"]==self.trump, x["card"]["suit"]==lead_suit, x["card"]["value"]))
            wi=self.players.index(next(p for p in self.players if p["user_id"]==winner["uid"]))
            self.tricks[winner["uid"]]+=1; self.trick=[]; self.leader=wi; self.turn=wi
            if len(hand)==0 and all(len(h)==0 for h in self.hands.values()):self.status="FINISHED"
        else:self.turn=(self.turn+1)%4
        self.deadline(20)
        return self.state(uid)
    def state(self,viewer=None):
        ps=[]
        for p in self.players:
            uid=p["user_id"]; x=self.public_player(p); x["bid"]=self.bids.get(uid); x["tricks"]=self.tricks.get(uid,0); x["hand"]=self.hands.get(uid,[]) if uid==viewer else "HIDDEN"; ps.append(x)
        return {"game":self.game_type,"status":self.status,"turn":self.turn,"deadline":self.turn_deadline,"trick":self.trick,"players":ps,"trump":self.trump}
