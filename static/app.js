const tg=window.Telegram?.WebApp;
const qs=s=>document.querySelector(s);
const GAMES=[["TEEN_PATTI","🎴","Teen Patti","2–6"],["RUMMY","🃏","Rummy","2–6"],["CALL_BREAK","♠️","Call Break","4"],["HAZARI","🔥","Hazari","2–4"],["ANDAR_BAHAR","🂡","Andar Bahar","1+"],["BLACKJACK","🎯","Blackjack","1–6"],["LUDO","🎲","Ludo","2–4"],["SNAKES_LADDERS","🐍","Snakes & Ladders","2–4"],["POKER_STYLE","♣️","Poker Style","2–6"]];
function miniReady(){try{tg?.ready();tg?.expand()}catch{}}
function uid(){return String(tg?.initDataUnsafe?.user?.id||localStorage.getItem("demo_uid")||("demo_"+Math.floor(Math.random()*1e8)))}
async function sync(){let id=uid();localStorage.setItem("demo_uid",id);let r=await fetch("/api/auth/telegram",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({initData:tg?.initData||"",demoUserId:id,demoName:tg?.initDataUnsafe?.user?.first_name||"Demo Player"})});return r.json()}
const RoyalLobby={async init(){miniReady();const auth=await sync();const u=auth.user;
qs("#app").innerHTML=`<div class="max-w-5xl mx-auto p-4 pb-20">
<header class="glass rounded-3xl p-5 flex items-center justify-between"><div><div class="text-2xl">👑 <span class="font-black gold">ROYAL GAMES</span></div><div class="text-xs text-slate-400">Ultimate Real-Time Social Games</div></div><div id="bal" class="px-4 py-2 rounded-xl bg-slate-950 border border-yellow-600 text-yellow-300 font-bold">🪙 ${u.coins.toLocaleString()}</div></header>
<section class="mt-6 grid md:grid-cols-3 gap-4">${GAMES.map(g=>`<button onclick="RoyalLobby.play('${g[0]}')" class="glass rounded-2xl p-5 text-left hover:scale-[1.01] transition"><div class="text-4xl">${g[1]}</div><div class="mt-3 text-lg font-bold">${g[2]}</div><div class="text-xs text-slate-400">${g[3]} players</div><div class="mt-2 inline-block text-[10px] px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300">● LIVE</div></button>`).join("")}</section>
<section class="mt-6 grid md:grid-cols-3 gap-4">
<div class="glass rounded-2xl p-5"><div class="font-bold text-yellow-300">🎁 Daily Reward</div><p class="text-sm text-slate-400 mt-1">Claim 100 virtual coins once per 24 hours.</p><button onclick="RoyalLobby.daily()" class="mt-4 px-4 py-2 rounded-xl bg-yellow-500 text-black font-bold">Claim</button></div>
<div class="glass rounded-2xl p-5"><div class="font-bold text-yellow-300">📺 Sponsor Reward</div><p class="text-sm text-slate-400 mt-1">Sponsored slot / rewarded promo.</p><button onclick="RoyalLobby.ad()" class="mt-4 px-4 py-2 rounded-xl bg-emerald-500 text-black font-bold">Watch</button></div>
<div class="glass rounded-2xl p-5"><div class="font-bold text-yellow-300">🏆 Tournament</div><p class="text-sm text-slate-400 mt-1">Virtual-coin tournaments and leaderboards.</p><a href="/api/tournaments" class="mt-4 inline-block px-4 py-2 rounded-xl bg-slate-800">View</a></div></section>
<section class="mt-6 glass rounded-2xl p-5"><div class="font-bold">Join Room</div><div class="flex gap-2 mt-3"><input id="room" maxlength="6" class="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 uppercase" placeholder="ROOM CODE"><button onclick="RoyalLobby.join()" class="px-5 rounded-xl bg-yellow-500 text-black font-bold">Join</button></div></section>
</div>`;
},
play(game){const room=Math.random().toString(36).slice(2,8).toUpperCase();location.href=`/play?game=${game}&room=${room}`},
join(){const r=qs("#room").value.trim().toUpperCase();if(r.length===6)location.href=`/play?game=TEEN_PATTI&room=${r}`},
async daily(){const r=await fetch(`/api/player/${uid()}/daily`,{method:"POST"});alert(JSON.stringify(await r.json()))},
async ad(){const r=await fetch("/api/ads/claim",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({userId:uid()})});alert(JSON.stringify(await r.json()))}}
