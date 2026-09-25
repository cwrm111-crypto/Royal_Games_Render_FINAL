import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
MINI = (os.getenv("MINI_APP_URL") or os.getenv("ROYAL_GAMES_APP_URL") or "").rstrip("/")

GAMES = [
    ("🎴 Teen Patti", "TEEN_PATTI"),
    ("🃏 Rummy", "RUMMY"),
    ("♠️ Call Break", "CALL_BREAK"),
    ("🔥 Hazari", "HAZARI"),
    ("🂡 Andar Bahar", "ANDAR_BAHAR"),
    ("🎯 Blackjack", "BLACKJACK"),
    ("🎲 Ludo", "LUDO"),
    ("🐍 Snakes & Ladders", "SNAKES_LADDERS"),
    ("♣️ Poker Style", "POKER_STYLE"),
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
        [InlineKeyboardButton("🎮 OPEN ROYAL GAMES", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton("🎴 Teen Patti LIVE", web_app=WebAppInfo(url=web_url("TEEN_PATTI")))],
        [InlineKeyboardButton("🃏 Rummy", web_app=WebAppInfo(url=web_url("RUMMY")))],
        [InlineKeyboardButton("♠️ Call Break", web_app=WebAppInfo(url=web_url("CALL_BREAK")))],
        [InlineKeyboardButton("🔥 Hazari", web_app=WebAppInfo(url=web_url("HAZARI")))],
        [InlineKeyboardButton("🂡 Andar Bahar", web_app=WebAppInfo(url=web_url("ANDAR_BAHAR")))],
        [InlineKeyboardButton("🎲 Ludo", web_app=WebAppInfo(url=web_url("LUDO")))],
    ])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 ROYAL GAMES\n\n"
        "🎮 Real-time multiplayer social games\n"
        "🪙 Virtual coins only\n\n"
        "নিচের game button চাপুন এবং Mini App থেকে live table-এ ঢুকুন।",
        reply_markup=lobby_menu(),
    )

async def play(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await start(update, ctx)

async def games(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = "🎮 GAME CENTER\n\n" + "\n".join(f"{i+1}. {name}" for i, (name, _) in enumerate(GAMES))
    await update.message.reply_text(text, reply_markup=lobby_menu())

async def mining(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛏️ VIRTUAL REWARD CENTER\n\n"
        "Mini App-এর Sponsor Reward section থেকে eligible virtual reward claim করুন।",
        reply_markup=lobby_menu(),
    )

async def wallet(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🪙 আপনার live virtual-coin balance Mini App-এর উপরে দেখা যাবে।",
        reply_markup=lobby_menu(),
    )

async def status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Royal Games V5 bot online.\n🎮 Mini App থেকে live games খুলুন।",
        reply_markup=lobby_menu(),
    )

async def help_(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — Game Lobby\n"
        "/play — Open Games\n"
        "/games — Game Center\n"
        "/mining — Virtual Rewards\n"
        "/wallet — Balance\n"
        "/status — Server Status\n"
        "/help — Help",
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
