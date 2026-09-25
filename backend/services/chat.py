class ChatModeration:
    BLOCKED={'spam-link','scam'}
    def clean(self, text): return ' '.join(w for w in text.split() if w.lower() not in self.BLOCKED)
