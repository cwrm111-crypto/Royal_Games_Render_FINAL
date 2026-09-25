# Telegram Live Game Setup

1. Run `scripts/start.ps1`.
2. Obtain a public HTTPS URL that forwards to port 8091. A temporary Cloudflare Tunnel can be used for testing with `scripts/start-public-tunnel.ps1` if `cloudflared` is installed.
3. Put that HTTPS URL into `.env` as `MINI_APP_URL`.
4. Run `scripts/start-bot.ps1`.
5. In Telegram use `/start`, `/play`, or `/games`. The bot now shows direct game buttons.

For production, use a stable HTTPS reverse proxy/domain and keep secrets only in `.env`. Do not use localhost or `0.0.0.0` as the Telegram Mini App URL.

All game balances in this project are virtual/social coins. No cash-out or real-money wagering is implemented.
