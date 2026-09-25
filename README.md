# Royal Games Ultimate — Render-ready V6 package

Royal Games is a local-first Telegram Mini App + real-time multiplayer social game platform using **virtual/social coins only**.

## Included games

Teen Patti, Rummy, Call Break, Hazari, Andar Bahar, Blackjack, Ludo, Snakes & Ladders, Poker Style.

## Final deployment architecture

- `royal-games-web`: FastAPI + python-socketio game server.
- `royal-games-bot`: Telegram polling worker.
- Render public HTTPS URL is used by the Telegram Mini App.
- SQLite is stored on a Render persistent disk at `/var/data/royal_games.sqlite3`.
- Render Blueprint configuration is included in `render.yaml`.
- One web instance is configured because game-room state is currently held in process memory and the persistent disk cannot be combined with horizontal scaling.

## Local run

```powershell
Set-ExecutionPolicy -Scope Process Bypass -Force
.\scripts\install.ps1
.\scripts\start.ps1
```

Default local URL: `http://127.0.0.1:8091`.

## Render deployment

1. Create a Git repository from this package and push the project.
2. In Render, create a **New Blueprint Instance** from that repository.
3. Render will provision the web service and Telegram background worker from `render.yaml`.
4. During the first Blueprint sync, enter `TELEGRAM_BOT_TOKEN` when Render asks for the secret.
5. After deployment, use the generated Render HTTPS URL as the Telegram Mini App URL. The bot worker receives it automatically from the web service.

The web service start command is:

```text
uvicorn backend.app:application --host 0.0.0.0 --port $PORT
```

The bot worker start command is:

```text
python bot/telegram_bot.py
```

## Telegram 409 warning

Do not run the same bot token with the local polling script and the Render worker at the same time. Only one `getUpdates` polling owner should be active.

## Safety / economy model

The project uses virtual/social coins only. It does **not** implement real-money wagering, crypto wagering, deposits, withdrawals, or cash-out.
