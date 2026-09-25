import threading
class WalletLock:
    def __init__(self): self._locks={}
    def lock(self, uid):
        self._locks.setdefault(str(uid), threading.Lock()); return self._locks[str(uid)]
