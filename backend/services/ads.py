import time, hmac, hashlib, os
from backend import db

class RewardedAdService:
    def __init__(self):
        self.reward=int(os.getenv("AD_REWARD_COINS","50"))
        self.cooldown=int(os.getenv("AD_REWARD_COOLDOWN_SEC","60"))
        self.last={}

    def claim(self,user_id,signature=None):
        now=time.time(); uid=str(user_id)
        if now-self.last.get(uid,0)<self.cooldown:
            return {"success":False,"message":"Reward cooldown active"}
        # This service is a local reward boundary. Real ad-provider verification must happen
        # server-to-server before production crediting.
        self.last[uid]=now
        n=db.adjust_coins(uid,self.reward,"AD_REWARD","Sponsored/rewarded promotion")
        return {"success":n is not None,"coins":n or 0,"reward":self.reward}
