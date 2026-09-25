import os, asyncio, json, time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import socketio
from dotenv import load_dotenv
from backend import db
from backend.games.registry import new_game
from backend.api.auth import router as auth_router
from backend.api.player import router as player_router
from backend.api.admin import router as admin_router
from backend.api.ads import router as ads_router
from backend.services.wallet import WalletService
from backend.services.tournaments import TournamentService

load_dotenv()
db.init_db()
app=FastAPI(title="Royal Games Ultimate V5",version="5.0.0")
sio=socketio.AsyncServer(async_mode="asgi",cors_allowed_origins="*")
app.mount("/static",StaticFiles(directory="static"),name="static")
app.include_router(auth_router);app.include_router(player_router);app.include_router(admin_router);app.include_router(ads_router)
games={}
wallet=WalletService(sio); tournaments=TournamentService()

async def state_for(game, viewer=None):
    try:
        s = game.state(viewer)
    except TypeError:
        s = game.state()
    if isinstance(s, dict) and isinstance(s.get("players"), list):
        for pl in s["players"]:
            uid = pl.get("user_id")
            if uid:
                u = db.get_user(uid)
                if u:
                    pl["coins"] = int(u["coins"])
    return s

async def emit_state(room_id, game, viewer=None):
    s = await state_for(game, viewer)
    db.set_room(room_id, game.game_type, game.status, s)
    await sio.emit("game_state", s, room=room_id)
    return s

async def settle_finished(game):
    if getattr(game, "settled", False) or game.status != "FINISHED":
        return
    if game.game_type == "TEEN_PATTI" and getattr(game, "winner_uid", None):
        await wallet.credit(game.winner_uid, game.pot, "GAME_WIN", f"Teen Patti room {game.room_id}")
    elif game.game_type == "HAZARI" and getattr(game, "winner_uid", None):
        await wallet.credit(game.winner_uid, game.pot, "GAME_WIN", f"Hazari room {game.room_id}")
    elif game.game_type == "BLACKJACK":
        for uid, result in getattr(game, "results", {}).items():
            if result == "WIN":
                await wallet.credit(uid, int(game.bets.get(uid, 0)) * 2, "GAME_WIN", f"Blackjack room {game.room_id}")
    elif game.game_type == "ANDAR_BAHAR" and getattr(game, "winner_side", None):
        for uid in game.bets.get(game.winner_side, {}):
            await wallet.push(uid)
    game.settled = True

@app.get("/")
async def root(): return FileResponse("static/index.html")
@app.get("/play")
async def play(): return FileResponse("static/game.html")
@app.get("/admin")
async def admin(): return FileResponse("static/admin.html")
@app.get("/health")
async def health(): return {"status":"ok","version":"5.0.0","games":len(games),"ollama":True}
@app.get("/api/games")
async def catalog(): return json.load(open("config/game_catalog.json",encoding="utf-8"))
@app.get("/api/leaderboard")
async def leaderboard(): return {"top":db.leaderboard(100)}
@app.get("/api/tournaments")
async def tourneys(): return {"tournaments":tournaments.list()}

async def add_user_room(uid):
    await sio.enter_room("",f"user:{uid}")

@sio.event
async def connect(sid,environ):
    print("CONNECT",sid)
@sio.event
async def disconnect(sid):
    print("DISCONNECT",sid)

@sio.event
async def user_subscribe(sid,data):
    uid=str(data.get("userId","")); await sio.enter_room(sid,f"user:{uid}")
    u=db.ensure_user(uid,data.get("name","Player"),data.get("username"))
    await sio.emit("wallet_update",{"user_id":uid,"coins":u["coins"]},to=sid)

@sio.event
async def join_room(sid,data):
    game_type=data.get("gameType","TEEN_PATTI"); room_id=str(data.get("roomId","")).upper()
    uid=str(data.get("userId") or sid); name=data.get("name","Player")
    u=db.ensure_user(uid,name,data.get("username"))
    if u.get("banned"): return await sio.emit("error_message",{"message":"Account banned"},to=sid)
    game=games.get(room_id)
    if not game: game=new_game(game_type,room_id);games[room_id]=game
    await sio.enter_room(sid,room_id);await sio.enter_room(sid,f"user:{uid}")
    game.add_player({"sid":sid,"user_id":uid,"name":name,"username":data.get("username","")})
    await emit_state(room_id, game, uid)
    await sio.emit("wallet_update",{"user_id":uid,"coins":u["coins"]},to=sid)

@sio.event
async def start_game(sid,data):
    rid=str(data.get("roomId","")).upper();game=games.get(rid)
    if not game:return
    if game.start():
        await emit_state(rid, game)

def debit_sync(uid,amt):
    # Socket handlers are single event-loop tasks; the service lock is used around
    # async wallet flows in dedicated helpers below.
    u=db.get_user(uid)
    if not u or u["coins"]<amt:return None
    return db.adjust_coins(uid,-amt,"GAME_BET","Virtual coin game action")

@sio.event
async def player_action(sid,data):
    rid=str(data.get("roomId","")).upper();act=data.get("action","");uid=str(data.get("userId") or sid);game=games.get(rid)
    if not game:return
    result=None
    # specialized async path for shared wallet
    if game.game_type=="TEEN_PATTI":
        before=game.state()
        # apply manually to preserve wallet source of truth
        if act.upper() in ("BLIND","CHAAL"):
            p=next((p for p in game.players if p["user_id"]==uid),None)
            if not p or game.players[game.turn]["user_id"]!=uid:return
            amount=game.current_bet*(2 if uid in game.seen else 1)
            if await wallet.debit(uid,amount,"GAME_BET",f"Teen Patti {act}") is None:return
            p["bet"]=p.get("bet",0)+amount;game.pot+=amount;game.current_bet=amount;game.next_turn()
            result=game.state(game.status=="FINISHED")
        else:
            result=game.action(uid,act,lambda _uid,_amt: True)
    elif game.game_type=="HAZARI":
        if act in ("CALL","PACK"):
            result=game.action(uid,act,lambda _uid,amt: debit_sync(_uid,amt))
    elif game.game_type=="ANDAR_BAHAR":
        if act.startswith("BET_"):
            result=game.bet(uid,act.split("_",1)[1].lower(),int(data.get("amount",10)),lambda _uid,amt: debit_sync(_uid,amt))
        elif act=="DEAL":result=game.deal()
        elif act=="STEP":result=game.step(lambda _uid,amt: db.adjust_coins(_uid,amt,"GAME_WIN","Andar Bahar virtual payout"))
    elif game.game_type=="BLACKJACK":
        if act=="BET":result=game.bet(uid,int(data.get("amount",10)),lambda _uid,amt: debit_sync(_uid,amt))
        elif act=="START":result=game.start()
        elif act=="HIT":result=game.hit(uid)
        elif act=="STAND":result=game.stand(uid)
    elif game.game_type=="RUMMY":
        if act=="DRAW":result=game.draw(uid,data.get("source","DECK"))
        elif act=="DISCARD":result=game.discard_card(uid,int(data.get("index",0)))
        elif act=="DECLARE":result=game.declare(uid)
    elif game.game_type=="CALL_BREAK":
        if act=="BID":result=game.bid(uid,int(data.get("bid",1)))
        elif act=="PLAY_CARD":result=game.play_card(uid,int(data.get("index",0)))
    elif game.game_type=="LUDO":
        if act=="ROLL":result=game.roll(uid)
        elif act=="MOVE":result=game.move(uid,int(data.get("token",0)))
    elif game.game_type=="SNAKES_LADDERS":
        if act=="ROLL":result=game.roll(uid)
    elif game.game_type=="POKER_STYLE":
        if act=="SHOW":result=game.showdown()
    if result is not None:
        if isinstance(result, dict) and result.get("error"):
            await sio.emit("error_message", {"message": result["error"]}, to=sid)
            return
        if game.status == "FINISHED":
            await settle_finished(game)
        await emit_state(rid, game, uid)
        await wallet.push(uid)

@sio.event
async def timer_ping(sid,data):
    rid=str(data.get("roomId","")).upper();game=games.get(rid)
    if not game or not game.turn_deadline:return
    if time.time()<game.turn_deadline:return
    if game.game_type=="TEEN_PATTI": result=game.timeout()
    elif hasattr(game,"timeout"): result=game.timeout()
    else: result=None
    if result:
        if game.status == "FINISHED":
            await settle_finished(game)
        await emit_state(rid, game)

application=socketio.ASGIApp(sio,app)
