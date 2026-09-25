from fastapi import APIRouter,Request
from backend.services.ads import RewardedAdService
router=APIRouter(prefix="/api/ads",tags=["ads"]); service=RewardedAdService()
@router.post("/claim")
async def claim(r:Request):
    d=await r.json(); uid=str(d.get("userId",""))
    if not uid:return {"success":False,"message":"userId required"}
    return service.claim(uid)
