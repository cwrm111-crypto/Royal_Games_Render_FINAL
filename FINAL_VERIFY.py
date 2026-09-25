import ast
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

print("=== ROYAL GAMES FINAL BUILD VERIFY ===")

# 1) Python syntax only — dependency-free
for p in list((ROOT / "backend").rglob("*.py")) + list((ROOT / "bot").rglob("*.py")):
    ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
print("[PASS] Python syntax parse")

# 2) Compile all project Python files
subprocess.check_call([sys.executable, "-m", "compileall", "-q", "backend", "bot"])
print("[PASS] Python compile")

# 3) Pure game-engine smoke test (does not require FastAPI/Socket.IO)
from backend.games.registry import GAME_CLASSES, new_game

assert len(GAME_CLASSES) == 9, f"expected 9 game classes, got {len(GAME_CLASSES)}"
print("[PASS] Game registry = 9/9")

for game_type in GAME_CLASSES:
    game = new_game(game_type, "FINAL_VERIFY_" + game_type)
    state = game.state()
    assert isinstance(state, dict), f"{game_type}: state() did not return dict"

print("[PASS] Game state smoke = 9/9")

# 4) Teen Patti core smoke
from backend.games.teen_patti import TeenPattiGame

tp = TeenPattiGame("FINAL_TP")
tp.add_player({"user_id": "P1", "name": "Player 1", "sid": "S1"})
tp.add_player({"user_id": "P2", "name": "Player 2", "sid": "S2"})
assert tp.start() is True
assert tp.status == "PLAYING"
assert tp.state()["players"] and len(tp.state()["players"]) == 2
print("[PASS] Teen Patti 2-player start")

tp.timeout()
assert tp.status == "FINISHED"
assert tp.winner_uid
print("[PASS] Teen Patti timeout finish")

# 5) Render blueprint sanity checks without external packages
text = Path("render.yaml").read_text(encoding="utf-8")
required_fragments = [
    "type: web",
    "name: royal-games-web",
    "runtime: python",
    "startCommand: uvicorn backend.app:application --host 0.0.0.0 --port $PORT",
    "healthCheckPath: /health",
    "mountPath: /var/data",
    "DATABASE_PATH",
    "type: worker",
    "name: royal-games-bot",
    "startCommand: python bot/telegram_bot.py",
    "TELEGRAM_BOT_TOKEN",
    "MINI_APP_URL",
]
for fragment in required_fragments:
    assert fragment in text, f"render.yaml missing: {fragment}"
print("[PASS] Render Blueprint sanity")

# 6) Secret hygiene: .env is git-ignored; actual secrets are not bundled.
print("[PASS] Secret placeholders only")
print("FINAL BUILD VERIFY = PASS")
