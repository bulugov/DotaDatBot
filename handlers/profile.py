from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from opendota.api import get_player_info, get_player_win_loss, rank_tier_to_name
from utils.userdata import get_linked_account

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    account_id = get_linked_account(telegram_id)

    if not account_id:
        await update.message.reply_text("❌ You haven't linked your Dota account yet. Use /link <account_id>")
        return

    info = get_player_info(account_id)
    wl = get_player_win_loss(account_id)

    if not info or not wl:
        await update.message.reply_text("⚠️ Could not fetch profile data. Please try again later.")
        return

    total_matches = wl['win'] + wl['lose']
    winrate = round((wl['win'] / total_matches) * 100, 2) if total_matches > 0 else 0
    rank = rank_tier_to_name(info.get('rank_tier'))

    profile_text = (
        f"👤 Profile: {info['profile']['personaname']}\n"
        f"📈 MMR Estimate: {info['mmr_estimate']['estimate']}\n"
        f"🏆 Winrate: {winrate}% ({wl['win']}W / {wl['lose']}L)\n"
        f"🎖️ Rank: {rank}"
    )
    await update.message.reply_text(profile_text)

handler = CommandHandler("profile", profile)
