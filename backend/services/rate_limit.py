import time
class RateLimiter:
    def __init__(self, window=1.0, limit=10): self.window=window; self.limit=limit; self.hits={}
    def allow(self, key):
        now=time.time(); arr=[t for t in self.hits.get(key,[]) if now-t<self.window]
        if len(arr)>=self.limit: self.hits[key]=arr; return False
        arr.append(now); self.hits[key]=arr; return True
