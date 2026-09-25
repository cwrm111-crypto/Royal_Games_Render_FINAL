from datetime import datetime, timedelta
class RewardService:
    def __init__(self): self.claims={}
    def claim(self, uid, amount=100):
        now=datetime.utcnow(); last=self.claims.get(str(uid))
        if last and now-last < timedelta(hours=24): return False
        self.claims[str(uid)]=now; return amount
