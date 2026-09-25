import time
class TurnTimer:
    def __init__(self, seconds=15): self.seconds=seconds; self.deadline=0
    def start(self): self.deadline=time.time()+self.seconds; return self.deadline
    def remaining(self): return max(0, self.deadline-time.time())
    def expired(self): return self.remaining()<=0
