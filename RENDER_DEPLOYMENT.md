# Royal Games — Render Deployment

This package is prepared for a Render Blueprint deployment.

## Architecture

- `royal-games-web`: FastAPI + Socket.IO game server.
- `royal-games-bot`: Telegram polling worker.
- A persistent Render disk is mounted at `/var/data` and SQLite is stored there.
- Render supplies the public HTTPS URL; Cloudflare Quick Tunnel is not required for the deployed service.
- Keep `numInstances: 1` because the current game-room state is in process memory and the SQLite disk cannot be combined with horizontal scaling.

## Required secret

During the first Blueprint sync, Render will prompt for `TELEGRAM_BOT_TOKEN`. Do not commit the real token to Git.

## Telegram

The bot worker receives `MINI_APP_URL` from the web service's Render external URL. After the web service is live, the bot's Mini App buttons use that Render URL.

If the same Telegram bot is still polling from a local PC, stop the local bot first. Otherwise Telegram can return HTTP 409 (`getUpdates` conflict).

## Start commands

Web service:

```text
uvicorn backend.app:application --host 0.0.0.0 --port $PORT
```

Worker:

```text
python bot/telegram_bot.py
```

## Important

The project intentionally uses virtual/social coins only. It does not implement real-money wagering, crypto wagering, deposits, withdrawals, or cash-out.

Render web services must listen on `0.0.0.0:$PORT`, and `/health` is configured as the health check. See the Render documentation for web service port binding and health checks.
