from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from opendota.api import get_latest_match
from utils.userdata import get_linked_account
from utils.heroes import load_hero_dict, hero_dict

load_hero_dict()


async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    account_id = context.args[0] if context.args else get_linked_account(telegram_id)
    if not account_id:
        await update.message.reply_text(
            "❌ You haven't linked your Dota account yet. Use /link <account_id>"
        )
        return

    match = get_latest_match(account_id)
    if not match:
        await update.message.reply_text("⚠️ No recent match found.")
        return

    hero_name = hero_dict.get(match["hero_id"], "Unknown Hero")
    kda = f"{match['kills']}/{match['deaths']}/{match['assists']}"
    win = (match["player_slot"] < 128 and match["radiant_win"]) or (
        match["player_slot"] >= 128 and not match["radiant_win"]
    )
    result = "Win" if win else "Loss"

    await update.message.reply_text(
        f"Hero: {hero_name}\nK/D/A: {kda}\nResult: {result}"
    )


handler = CommandHandler("match", match)
