class NotificationService:
    def __init__(self): self.outbox=[]
    def push(self, uid, title, body): self.outbox.append({'uid':str(uid),'title':title,'body':body})
