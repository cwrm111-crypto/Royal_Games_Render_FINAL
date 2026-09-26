import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
MINI = (os.getenv("MINI_APP_URL") or os.getenv("ROYAL_GAMES_APP_URL") or os.getenv("RENDER_EXTERNAL_URL") or "").rstrip("/")

GAMES = [
    ("ðŸŽ´ Teen Patti", "TEEN_PATTI"),
    ("ðŸƒ Rummy", "RUMMY"),
    ("â™ ï¸ Call Break", "CALL_BREAK"),
    ("ðŸ”¥ Hazari", "HAZARI"),
    ("ðŸ‚¡ Andar Bahar", "ANDAR_BAHAR"),
    ("ðŸŽ¯ Blackjack", "BLACKJACK"),
    ("ðŸŽ² Ludo", "LUDO"),
    ("ðŸ Snakes & Ladders", "SNAKES_LADDERS"),
    ("â™£ï¸ Poker Style", "POKER_STYLE"),
]

def web_url(game=None):
    if not MINI:
        return None
    if game:
        return f"{MINI}/play?game={game}"
    return MINI

def lobby_menu():
    url = web_url()
    if not url:
        return None
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ðŸŽ® OPEN ROYAL GAMES", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton("ðŸŽ´ Teen Patti LIVE", web_app=WebAppInfo(url=web_url("TEEN_PATTI")))],
        [InlineKeyboardButton("ðŸƒ Rummy", web_app=WebAppInfo(url=web_url("RUMMY")))],
        [InlineKeyboardButton("â™ ï¸ Call Break", web_app=WebAppInfo(url=web_url("CALL_BREAK")))],
        [InlineKeyboardButton("ðŸ”¥ Hazari", web_app=WebAppInfo(url=web_url("HAZARI")))],
        [InlineKeyboardButton("ðŸ‚¡ Andar Bahar", web_app=WebAppInfo(url=web_url("ANDAR_BAHAR")))],
        [InlineKeyboardButton("ðŸŽ² Ludo", web_app=WebAppInfo(url=web_url("LUDO")))],
    ])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ðŸ‘‘ ROYAL GAMES\n\n"
        "ðŸŽ® Real-time multiplayer social games\n"
        "ðŸª™ Virtual coins only\n\n"
        "à¦¨à¦¿à¦šà§‡à¦° game button à¦šà¦¾à¦ªà§à¦¨ à¦à¦¬à¦‚ Mini App à¦¥à§‡à¦•à§‡ live table-à¦ à¦¢à§à¦•à§à¦¨à¥¤",
        reply_markup=lobby_menu(),
    )

async def play(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await start(update, ctx)

async def games(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = "ðŸŽ® GAME CENTER\n\n" + "\n".join(f"{i+1}. {name}" for i, (name, _) in enumerate(GAMES))
    await update.message.reply_text(text, reply_markup=lobby_menu())

async def mining(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "â›ï¸ VIRTUAL REWARD CENTER\n\n"
        "Mini App-à¦à¦° Sponsor Reward section à¦¥à§‡à¦•à§‡ eligible virtual reward claim à¦•à¦°à§à¦¨à¥¤",
        reply_markup=lobby_menu(),
    )

async def wallet(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ðŸª™ à¦†à¦ªà¦¨à¦¾à¦° live virtual-coin balance Mini App-à¦à¦° à¦‰à¦ªà¦°à§‡ à¦¦à§‡à¦–à¦¾ à¦¯à¦¾à¦¬à§‡à¥¤",
        reply_markup=lobby_menu(),
    )

async def status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "âœ… Royal Games V5 bot online.\nðŸŽ® Mini App à¦¥à§‡à¦•à§‡ live games à¦–à§à¦²à§à¦¨à¥¤",
        reply_markup=lobby_menu(),
    )

async def help_(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start â€” Game Lobby\n"
        "/play â€” Open Games\n"
        "/games â€” Game Center\n"
        "/mining â€” Virtual Rewards\n"
        "/wallet â€” Balance\n"
        "/status â€” Server Status\n"
        "/help â€” Help",
        reply_markup=lobby_menu(),
    )

def main():
    if not TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is empty in .env")
    app = Application.builder().token(TOKEN).build()
    for cmd, fn in [
        ("start", start), ("play", play), ("games", games),
        ("mining", mining), ("wallet", wallet), ("status", status),
        ("help", help_),
    ]:
        app.add_handler(CommandHandler(cmd, fn))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

