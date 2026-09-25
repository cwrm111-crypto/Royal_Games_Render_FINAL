from .common import BaseGame, deck
class BlackjackGame(BaseGame):
    game_type="BLACKJACK"; max_players=6
    def __init__(self,room_id):super().__init__(room_id);self.hands={};self.bets={};self.stood=set();self.dealer=[];self.deck=[]
    def total(self,hand):
        total=sum(min(c["value"],10) for c in hand); aces=sum(c["rank"]=="A" for c in hand)
        while total>21 and aces: total-=10;aces-=1
        return total
    def bet(self,uid,amt,wallet_debit):
        if self.status not in ("WAITING","BETTING") or amt<=0:return None
        if wallet_debit(uid,amt) is None:return {"error":"INSUFFICIENT_COINS"}
        self.bets[uid]=amt;self.status="BETTING";return self.state(uid)
    def start(self):
        if not self.bets:return False
        self.deck=deck();self.dealer=[self.deck.pop(),self.deck.pop()];self.hands={uid:[self.deck.pop(),self.deck.pop()] for uid in self.bets};self.stood=set();self.results={};self.settled=False;self.status="PLAYING";self.deadline(20);return True
    def hit(self,uid):
        if self.status!="PLAYING" or uid in self.stood:return None
        self.hands[uid].append(self.deck.pop()); 
        if self.total(self.hands[uid])>21:self.stood.add(uid)
        if all(uid in self.stood for uid in self.hands):self.finish()
        return self.state(uid)
    def stand(self,uid):
        if self.status!="PLAYING":return None
        self.stood.add(uid)
        if all(uid in self.stood for uid in self.hands):self.finish()
        return self.state(uid)
    def finish(self):
        while self.total(self.dealer)<17:self.dealer.append(self.deck.pop())
        dealer_total=self.total(self.dealer)
        self.status="FINISHED"; self.results={}
        for uid,hand in self.hands.items():
            t=self.total(hand); bet=self.bets[uid]
            self.results[uid]="LOSE"
            if t<=21 and (dealer_total>21 or t>dealer_total):self.results[uid]="WIN"
        return self.results
    def state(self,viewer=None):
        return {"game":self.game_type,"status":self.status,"dealer":self.dealer if self.status=="FINISHED" else self.dealer[:1],
                "players":[{**self.public_player(p),"hand":self.hands.get(p["user_id"],[]) if p["user_id"]==viewer or self.status=="FINISHED" else "HIDDEN","bet":self.bets.get(p["user_id"],0)} for p in self.players]}
