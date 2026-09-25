from fastapi import APIRouter, Request
import os
from backend.services.telegram_auth import verify_init_data
from backend import db
router=APIRouter(prefix="/api/auth",tags=["auth"])
@router.post("/telegram")
async def telegram_auth(request:Request):
    d=await request.json(); bot=os.getenv("TELEGRAM_BOT_TOKEN","")
    user=verify_init_data(d.get("initData",""),bot) if d.get("initData") else None
    if not user:
        uid=str(d.get("demoUserId") or "demo_user"); name=d.get("demoName","Demo Player"); username=""
    else:
        uid=str(user.get("id"));name=user.get("first_name","Player");username=user.get("username","")
    u=db.ensure_user(uid,name,username,int(os.getenv("START_COINS","5000")))
    return {"success":True,"user":u}
