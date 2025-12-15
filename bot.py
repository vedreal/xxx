import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

# Konfigurasi
BOT_TOKEN = "8500107504:AAFjjAjIb6k9Hdm8QiUoyGUFiIB8x0dMNNs"
ADMIN_USER_IDS = [6384292054]  # Ganti dengan user ID admin Anda
DATA_FILE = "users.json"

# Load/Save user data
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

users_db = load_users()

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    # Check if new user
    if user_id not in users_db:
        users_db[user_id] = {
            "username": user.username,
            "first_name": user.first_name,
            "joined_at": update.message.date.isoformat()
        }
        save_users(users_db)
        print(f"[NEW USER] {user.first_name} (@{user.username}) - ID: {user.id}")
    
    welcome_text = """*Welcome to SYDAI ✨*

SYDAI is an AI\\-powered, chat\\-based platform built on blockchain technology,
designed to create a transparent and community\\-driven crypto ecosystem\\.

Our vision is to combine artificial intelligence and blockchain into a single
interactive platform where users are rewarded for participation, consistency,
and long\\-term engagement\\.

*With SYDAI, users can:*
• Earn points through daily check\\-ins and verified tasks
• Participate in community and referral\\-based growth programs
• Access upcoming AI\\-powered crypto features and utilities
• Accumulate points that may be converted into SYDAI token rewards via airdrop

*SYDAI is built with a long\\-term mindset:*
– Fair and transparent point distribution
– Anti\\-abuse and verification systems
– On\\-chain readiness for future token integration
– Continuous feature development and ecosystem expansion

Early users play a key role in shaping the SYDAI ecosystem\\.
Your activity, participation, and feedback directly contribute to the future
direction of the platform\\.

Start your journey today and become an early contributor to the SYDAI ecosystem 🚀"""
    
    # Button untuk mini app
    keyboard = [[InlineKeyboardButton("Get Points", url="https://t.me/sydaicoin_bot/app")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

# Command /broadcast (admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if admin
    if user_id not in ADMIN_USER_IDS:
        await update.message.reply_text("⛔ Only admin can use this command.")
        return
    
    # Check if message provided
    if not context.args:
        await update.message.reply_text(
            "Usage: /broadcast <message>\n\n"
            "Example: /broadcast Hello everyone! New update is live."
        )
        return
    
    # Get broadcast message
    broadcast_msg = " ".join(context.args)
    
    # Send to all users
    success = 0
    failed = 0
    
    for uid in users_db.keys():
        try:
            await context.bot.send_message(chat_id=int(uid), text=broadcast_msg)
            success += 1
        except Exception:
            failed += 1
    
    await update.message.reply_text(
        f"✅ Broadcast completed!\n"
        f"• Sent: {success}\n"
        f"• Failed: {failed}"
    )

def main():
    print("🤖 SYDAI Bot starting...")
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    
    print("✅ Bot is running...")
    print("📊 Press Ctrl+C to stop\n")
    
    # Run bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
