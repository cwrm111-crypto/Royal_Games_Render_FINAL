from collections import Counter
class Metrics:
    def __init__(self): self.c=Counter()
    def inc(self, name, n=1): self.c[name]+=n
    def snapshot(self): return dict(self.c)
