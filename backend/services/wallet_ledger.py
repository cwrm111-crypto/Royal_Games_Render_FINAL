from dataclasses import dataclass
from datetime import datetime
@dataclass
class LedgerEntry:
    user_id:str; amount:int; kind:str; note:str=''; at:str=''
class WalletLedger:
    def __init__(self): self.entries=[]
    def add(self, user_id, amount, kind, note=''):
        e=LedgerEntry(str(user_id),int(amount),kind,note,datetime.utcnow().isoformat()); self.entries.append(e); return e
    def for_user(self, uid): return [e for e in self.entries if e.user_id==str(uid)]
