from .common import BaseGame, deck
class AndarBaharGame(BaseGame):
    game_type="ANDAR_BAHAR"; max_players=6
    def __init__(self,room_id):super().__init__(room_id);self.bets={"andar":{},"bahar":{}};self.dealer=None;self.card=None;self.side_turn=0;self.winner_side=None
    def start(self):
        if not self.players:return False
        d=deck();self.dealer=d.pop();self.deck=d;self.bets={"andar":{},"bahar":{}};self.status="BETTING";self.deadline(20);return True
    def bet(self,uid,side,amount,wallet_debit):
        if self.status!="BETTING" or side not in self.bets or amount<=0:return None
        if wallet_debit(uid,amount) is None:return {"error":"INSUFFICIENT_COINS"}
        self.bets[side][uid]=self.bets[side].get(uid,0)+amount
        return self.state()
    def deal(self):
        if self.status!="BETTING":return None
        self.status="DEALING"; self.card=None; return self.state()
    def step(self,credit):
        if self.status!="DEALING":return None
        c=self.deck.pop(); self.card=c
        if c["value"]==self.dealer["value"]:
            self.status="FINISHED"; 
            # This keeps a deterministic virtual-payout rule for demo/social mode.
            side="andar" if sum(self.bets["andar"].values())>=sum(self.bets["bahar"].values()) else "bahar"
            self.winner_side=side
            for uid,amt in self.bets[side].items(): credit(uid,amt*2)
        return self.state()
    def state(self):
        return {"game":self.game_type,"status":self.status,"dealer":self.dealer,"card":self.card,"winner_side":self.winner_side,"bets":self.bets,"deadline":self.turn_deadline,"players":self.public_players()}
