from fastapi import APIRouter, HTTPException, Request
import os,secrets
from backend import db
router=APIRouter(prefix="/admin",tags=["admin"]); sessions={}
def token_ok(r): 
    t=r.headers.get("Authorization","").replace("Bearer ","")
    if t not in sessions: raise HTTPException(401,"Unauthorized")
@router.post("/login")
async def login(r:Request):
    d=await r.json()
    if d.get("password")!=os.getenv("ADMIN_PASSWORD","change_this_locally"):raise HTTPException(401,"Invalid password")
    t=secrets.token_urlsafe(24);sessions[t]=True;return {"token":t}
@router.get("/stats")
async def stats(r:Request):
    token_ok(r)
    users=db.leaderboard(100000);rooms=db.room_rows()
    return {"users":len(users),"rooms":len(rooms),"coins":sum(x["coins"] for x in users),"transactions":sum(len(db.transactions(x["id"],100000)) for x in users)}
@router.get("/rooms")
async def rooms(r:Request):token_ok(r);return {"rooms":db.room_rows()}
@router.get("/users")
async def users(r:Request):token_ok(r);return {"users":db.leaderboard(1000)}
