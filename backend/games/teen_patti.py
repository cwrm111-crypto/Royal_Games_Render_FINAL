from .common import deck
from .common import BaseGame

class TeenPatti:
    HIGH_CARD=1; PAIR=2; COLOR=3; SEQUENCE=4; PURE_SEQUENCE=5; TRAIL=6

def _eval(cards):
    s=sorted(cards,key=lambda c:c["value"],reverse=True)
    vals=[c["value"] for c in s]
    same=len({c["suit"] for c in s})==1
    seq=(vals[0]==vals[1]+1 and vals[1]==vals[2]+1)
    if vals==[14,3,2]: seq=True; seqhigh=3
    else: seqhigh=vals[0]
    if vals[0]==vals[1]==vals[2]: return TeenPatti.TRAIL,[vals[0]]
    if same and seq: return TeenPatti.PURE_SEQUENCE,[seqhigh]
    if seq: return TeenPatti.SEQUENCE,[seqhigh]
    if same: return TeenPatti.COLOR,*([vals] if False else (vals,))
    if vals[0]==vals[1]: return TeenPatti.PAIR,[vals[0],vals[2]]
    if vals[1]==vals[2]: return TeenPatti.PAIR,[vals[1],vals[0]]
    return TeenPatti.HIGH_CARD,vals

def compare(a,b):
    ra,va=_eval(a); rb,vb=_eval(b)
    if ra!=rb:return (ra>rb)-(ra<rb)
    return (va>vb)-(va<vb)

class TeenPattiGame(BaseGame):
    game_type="TEEN_PATTI"; max_players=6
    def __init__(self,room_id):
        super().__init__(room_id); self.pot=0; self.current_bet=10; self.round=0; self.cards={}; self.seen=set(); self.packed=set()
    def add_player(self,p):
        if super().add_player(p):
            p.setdefault("bet",0); return True
        return False
    def start(self):
        if len(self.players)<2:return False
        d=deck(); self.cards={p["user_id"]:[d.pop(),d.pop(),d.pop()] for p in self.players}
        self.seen=set(); self.packed=set(); self.pot=0; self.current_bet=10; self.turn=0; self.round+=1; self.status="PLAYING"; self.settled=False; self.winner_uid=None; self.deadline(15); return True
    def active(self): return [p for p in self.players if p["user_id"] not in self.packed]
    def action(self,uid,action,wallet_debit):
        if self.status!="PLAYING" or self.players[self.turn]["user_id"]!=uid:return None
        p=next((p for p in self.players if p["user_id"]==uid),None)
        if not p:return None
        a=action.upper()
        if a=="SEEN": self.seen.add(uid)
        elif a=="PACK": self.packed.add(uid)
        elif a in ("BLIND","CHAAL"):
            amount=self.current_bet*(2 if uid in self.seen else 1)
            if wallet_debit(uid,amount) is None:return {"error":"INSUFFICIENT_COINS"}
            p["bet"]=p.get("bet",0)+amount; self.pot+=amount; self.current_bet=amount
        elif a=="SHOW":
            active=self.active()
            if len(active)<2:return {"error":"NOT_ENOUGH_PLAYERS"}
            self.status="FINISHED"; self.finish()
            return self.state(True)
        else:return {"error":"INVALID_ACTION"}
        if len(self.active())<=1:
            self.status="FINISHED"; self.finish()
        else:self.next_turn()
        return self.state(self.status=="FINISHED")
    def next_turn(self):
        n=len(self.players)
        for _ in range(n):
            self.turn=(self.turn+1)%n
            if self.players[self.turn]["user_id"] not in self.packed: break
        self.deadline(15)
    def timeout(self):
        if self.status=="PLAYING":
            self.packed.add(self.players[self.turn]["user_id"])
            if len(self.active())<=1:self.status="FINISHED"; self.finish()
            else:self.next_turn()
            return self.state(self.status=="FINISHED")
    def finish(self):
        active=self.active()
        if not active:return
        winner=active[0]
        for p in active[1:]:
            if compare(self.cards[p["user_id"]],self.cards[winner["user_id"]])>0:winner=p
        winner["winner"]=True; self.winner_uid=winner["user_id"]
    def state(self,reveal=False):
        ps=[]
        for i,p in enumerate(self.players):
            x=self.public_player(p); x["seat"]=i; x["is_seen"]=p["user_id"] in self.seen; x["is_packed"]=p["user_id"] in self.packed; x["bet"]=p.get("bet",0)
            if reveal or self.status=="FINISHED": x["cards"]=self.cards.get(p["user_id"],[])
            elif p["user_id"]==self.players[self.turn]["user_id"] and p["user_id"] in self.cards: x["cards"]=self.cards[p["user_id"]]
            else:x["cards"]="HIDDEN"
            ps.append(x)
        return {"game":self.game_type,"status":self.status,"pot":self.pot,"turn":self.turn,"deadline":self.turn_deadline,"players":ps}
