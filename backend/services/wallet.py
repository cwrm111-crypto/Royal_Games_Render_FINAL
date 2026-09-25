import asyncio
from backend import db

class WalletService:
    def __init__(self, sio=None):
        self.sio=sio
        self._lock=asyncio.Lock()

    async def balance(self, user_id):
        return int((db.get_user(user_id) or {}).get("coins",0))

    async def credit(self, user_id, amount, tx_type, note=""):
        async with self._lock:
            n=db.adjust_coins(user_id,int(amount),tx_type,note)
        await self.push(user_id,n)
        return n

    async def debit(self, user_id, amount, tx_type, note=""):
        async with self._lock:
            u=db.get_user(user_id)
            if not u or int(u["coins"]) < int(amount):
                return None
            n=db.adjust_coins(user_id,-int(amount),tx_type,note)
        await self.push(user_id,n)
        return n

    async def push(self,user_id,balance=None):
        if not self.sio: return
        if balance is None: balance=await self.balance(user_id)
        await self.sio.emit("wallet_update", {"user_id":str(user_id),"coins":int(balance)}, room=f"user:{user_id}")

    async def settle_many(self, credits, tx_type="GAME_SETTLEMENT"):
        for uid, amount, note in credits:
            await self.credit(uid, amount, tx_type, note)
