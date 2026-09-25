from fastapi import APIRouter, HTTPException, Request
from datetime import datetime,timedelta
from backend import db
from backend.services.friends import FriendsService
router=APIRouter(prefix="/api/player",tags=["player"]); friends=FriendsService()
@router.get("/{uid}")
async def user(uid:str):
    u=db.get_user(uid)
    if not u: raise HTTPException(404,"User not found")
    return u
@router.get("/{uid}/transactions")
async def tx(uid:str): return {"transactions":db.transactions(uid)}
@router.post("/{uid}/daily")
async def daily(uid:str):
    u=db.get_user(uid)
    if not u: raise HTTPException(404)
    last=u.get("last_daily")
    if last and datetime.utcnow()-datetime.fromisoformat(last)<timedelta(hours=24): return {"success":False,"message":"Already claimed"}
    u=db.update_user(uid,coins=int(u["coins"])+100,xp=int(u["xp"])+10,last_daily=datetime.utcnow().isoformat())
    db.tx(uid,100,"DAILY_REWARD","Daily virtual reward")
    return {"success":True,"coins":u["coins"]}
@router.get("/{uid}/friends")
async def friend_list(uid:str): return {"friends":friends.list(uid)}
@router.post("/{uid}/friends/{fid}")
async def friend_add(uid:str,fid:str): return friends.add(uid,fid)
