import logging
import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
# PASTE YOUR TOKEN HERE
BOT_TOKEN = "8633914734:AAHCb01yBMbZd1Cpamcm6BNvsBTOaysGM3Y" 
PORT = int(os.environ.get("PORT", 8080))

# Your uploaded image direct link
HERO_PHOTO = "https://i.ibb.co/VcsGwvx8/IMG-20260306-WA0003.jpg"
GROUP_LINK = "https://t.me/hongdongofficial"

# ── Flask Server (Required for Render & UptimeRobot) ─────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return "Bot is alive! 🚀", 200

def run_flask():
    flask_app.run(host="0.0.0.0", port=PORT)

# ── Captions ─────────────────────────────────────────────────────────────────
WELCOME_CAPTION = (
    "🪂✨ <b>WELCOME TO HONGDONG AIRDROP BOT</b> ✨🪂\n\n"
    "🎉 <b>You've arrived at the official airdrop portal!</b>\n\n"
    "💎 <b>What is this?</b>\n"
    "Link your wallet and claim <b>exclusive FREE tokens</b>.\n\n"
    "🔥 <b>How it works:</b>\n"
    "1️⃣ Link your wallet\n"
    "2️⃣ Join the Telegram group\n"
    "3️⃣ Complete tasks\n"
    "4️⃣ Claim rewards!\n\n"
    "🌐 <b>Chains:</b> Solana • Ethereum • Base • BSC"
)

WALLET_CAPTION = (
    "🔗💼 <b>LINK YOUR WALLET</b> 💼🔗\n\n"
    "📋 <b>Choose your preferred blockchain:</b>\n"
    "🔒 <b>We never ask for private keys.</b>"
)

CHAIN_CAPTION = (
    "⛓️🎯 <b>WALLET SUBMISSION</b> 🎯⛓️\n\n"
    "<b>You selected: {chain}</b>\n\n"
    "📩 <b>Send your address as a message to this bot now.</b>\n\n"
    "Example: <code>0xYourWalletAddressHere</code>"
)

TASKS_CAPTION = (
    "📋🏆 <b>ELIGIBILITY TASKS</b> 🏆📋\n\n"
    "1️⃣ Join @hongdongofficial\n"
    "2️⃣ Follow announcements\n"
    "3️⃣ Link wallet\n"
    "4️⃣ Hold minimum balance"
)

FAQ_CAPTION = (
    "❓💡 <b>FAQ</b> 💡❓\n\n"
    "🔹 <b>Is it free?</b> Yes.\n"
    "🔹 <b>When distribution?</b> 24-72 hours.\n"
    "🔹 <b>How many?</b> One wallet per user."
)

SUPPORT_CAPTION = (
    "🛟📞 <b>SUPPORT</b> 📞🛟\n\n"
    "💬 Need help? Contact a moderator in @hongdongofficial\n"
    "⚠️ Admins will NEVER DM you first."
)

HELP_TEXT = "🆘 <b>HELP MENU</b>\n/start — Main portal\n/help — Show this message"

# ── Keyboard Builders ────────────────────────────────────────────────────────
def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗💰 Link My Wallet", callback_data="nav_wallet")],
        [InlineKeyboardButton("📋✅ Tasks", callback_data="nav_tasks"),
         InlineKeyboardButton("❓💡 FAQ", callback_data="nav_faq")],
        [InlineKeyboardButton("🌐 Join Community", url=GROUP_LINK)],
        [InlineKeyboardButton("🛟 Support", callback_data="nav_support")],
    ])

def kb_chains():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◎ Solana", callback_data="chain_sol"),
         InlineKeyboardButton("⟠ Ethereum", callback_data="chain_eth")],
        [InlineKeyboardButton("🔵 Base", callback_data="chain_base"),
         InlineKeyboardButton("🟡 BSC", callback_data="chain_bsc")],
        [InlineKeyboardButton("🔙 Back", callback_data="nav_home")],
    ])

def kb_back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="nav_home")],
    ])

def kb_chain_back(chain_label: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Different Chain", callback_data="nav_wallet")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="nav_home")],
    ])

# ── Core edit helper ─────────────────────────────────────────────────────────
async def refresh_screen(query, caption: str, keyboard: InlineKeyboardMarkup):
    try:
        media = InputMediaPhoto(media=HERO_PHOTO, caption=caption, parse_mode="HTML")
        await query.edit_message_media(media=media, reply_markup=keyboard)
    except Exception:
        # If photo link fails, edit current message as TEXT only
        try:
            await query.edit_message_text(text=caption, parse_mode="HTML", reply_markup=keyboard)
        except Exception as e:
            logger.error(f"Refresh screen failed: {e}")

# ── Handlers ──────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_photo(
            photo=HERO_PHOTO, 
            caption=WELCOME_CAPTION, 
            parse_mode="HTML", 
            reply_markup=kb_main()
        )
    except Exception:
        # Fallback to text if the image link is blocked or broken
        await update.message.reply_text(
            text=WELCOME_CAPTION, 
            parse_mode="HTML", 
            reply_markup=kb_main()
        )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="HTML")

async def route_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "nav_home":
        await refresh_screen(query, WELCOME_CAPTION, kb_main())
    elif data == "nav_wallet":
        await refresh_screen(query, WALLET_CAPTION, kb_chains())
    elif data == "nav_tasks":
        await refresh_screen(query, TASKS_CAPTION, kb_back())
    elif data == "nav_faq":
        await refresh_screen(query, FAQ_CAPTION, kb_back())
    elif data == "nav_support":
        await refresh_screen(query, SUPPORT_CAPTION, kb_back())
    elif data.startswith("chain_"):
        labels = {"chain_sol": "Solana", "chain_eth": "Ethereum", "chain_base": "Base", "chain_bsc": "BSC"}
        chain_name = labels.get(data, "Crypto")
        context.user_data["pending_chain"] = chain_name
        await refresh_screen(query, CHAIN_CAPTION.format(chain=chain_name), kb_chain_back(chain_name))

async def collect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = context.user_data.get("pending_chain")
    if not chain or (update.message.text and update.message.text.startswith("/")):
        return

    wallet = update.message.text.strip()
    context.user_data.pop("pending_chain", None)

    conf = f"✅ <b>LINKED!</b>\n⛓️ <b>Chain:</b> {chain}\n💼 <b>Address:</b> <code>{wallet}</code>"
    
    try:
        await update.message.reply_photo(photo=HERO_PHOTO, caption=conf, parse_mode="HTML", reply_markup=kb_back())
    except Exception:
        await update.message.reply_text(text=conf, parse_mode="HTML", reply_markup=kb_back())

# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Verify BOT_TOKEN is not default
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("PLEASE SET YOUR BOT_TOKEN IN THE CODE!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CallbackQueryHandler(route_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_wallet))
    
    logger.info("Bot is starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
