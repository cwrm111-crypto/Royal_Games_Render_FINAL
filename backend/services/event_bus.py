class EventBus:
    def __init__(self): self.listeners={}
    def on(self, name, fn): self.listeners.setdefault(name, []).append(fn)
    def emit(self, name, payload):
        for fn in self.listeners.get(name, []): fn(payload)
