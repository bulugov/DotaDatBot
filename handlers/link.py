from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.userdata import link_user

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /link <dota_account_id>")
        return

    telegram_id = update.effective_user.id
    dota_account_id = context.args[0]
    link_user(telegram_id, dota_account_id)

    await update.message.reply_text(f"✅ Linked your Telegram to Dota account ID {dota_account_id}.")

handler = CommandHandler("link", link)
