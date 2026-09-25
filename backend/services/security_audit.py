class SecurityAudit:
    def __init__(self): self.events=[]
    def log(self, event, actor='system'): self.events.append({'event':event,'actor':actor})
    def recent(self, n=100): return self.events[-n:]
