from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from opendota import get_latest_match, get_hero_dict, get_player_info, get_player_win_loss, rank_tier_to_name
from userdata import link_user, get_linked_account

BOT_TOKEN = "7924889946:AAEuaMJ34oYH7dnCg7BOQawuePR7q_ZFIBk"
OPEN_DOTA_URL = "https://api.opendota.com/api"

# Cache heroes when bot starts
hero_dict = get_hero_dict()

def get_latest_match(account_id):
    response = requests.get(f"{OPEN_DOTA_URL}/players/{account_id}/recentMatches")
    if response.status_code == 200:
        matches = response.json()
        return matches[0] if matches else None
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /match <account_id> to get your latest match.")

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if context.args:
        account_id = context.args[0]
    else:
        account_id = get_linked_account(telegram_id)
        if not account_id:
            await update.message.reply_text("❌ You haven't linked your Dota account yet. Use /link <account_id>")
            return
    match = get_latest_match(account_id)

    if match:
        win = (match['player_slot'] < 128 and match['radiant_win']) or (match['player_slot'] >= 128 and not match['radiant_win'])
        result = "Win" if win else "Loss"
        hero_name = hero_dict.get(match["hero_id"], f"Unknown Hero ({match['hero_id']})")
        msg = (
            f"Hero: {hero_name}\n"
            f"K/D/A: {match['kills']}/{match['deaths']}/{match['assists']}\n"
            f"Result: {result}"
        )
    else:
        msg = "No match found or error fetching data."

    await update.message.reply_text(msg)

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /link <dota_account_id>")
        return

    telegram_id = update.effective_user.id
    dota_account_id = context.args[0]

    link_user(telegram_id, dota_account_id)
    await update.message.reply_text(f"✅ Linked your Telegram to Dota account ID {dota_account_id}.")

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
        f"🧑 Profile: {info['profile']['personaname']}\n"
        f"🎮 Total Matches: {total_matches}\n"
        f"🏆 Wins: {wl['win']} / ❌ Losses: {wl['lose']}\n"
        f"📊 Win Rate: {winrate}%\n"
        f"🥇 Rank: {rank}"
    )

    await update.message.reply_text(profile_text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("match", match))
    app.add_handler(CommandHandler("link", link))
    app.run_polling()

