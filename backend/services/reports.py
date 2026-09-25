from collections import Counter
class ReportService:
    def __init__(self): self.items=[]
    def add(self, reporter, target, reason): self.items.append({'reporter':reporter,'target':target,'reason':reason})
    def counts(self): return Counter(x['reason'] for x in self.items)
