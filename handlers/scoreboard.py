from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from opendota.api import get_latest_match, get_match_details
from utils.userdata import get_linked_account
from utils.heroes import load_hero_dict, hero_dict, get_hero_icon

from PIL import Image, ImageDraw, ImageFont
import io

load_hero_dict()


async def scoreboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    account_id = get_linked_account(telegram_id)

    if not account_id:
        await update.message.reply_text(
            "❌ You haven't linked your Dota account yet. Use /link <account_id>"
        )
        return

    latest = get_latest_match(account_id)
    if not latest:
        await update.message.reply_text("⚠️ Could not fetch your latest match.")
        return

    match_id = latest["match_id"]
    match_data = get_match_details(match_id)
    if not match_data or "players" not in match_data:
        await update.message.reply_text("⚠️ Could not retrieve full match details.")
        return

    players = match_data["players"]
    row_height = 50
    img_width = 600
    img_height = row_height * len(players) + 20
    img = Image.new("RGB", (img_width, img_height), color=(34, 34, 34))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    for idx, p in enumerate(players):
        hero_name = hero_dict.get(p["hero_id"], f"Hero {p['hero_id']}")
        side = "Radiant" if p["player_slot"] < 128 else "Dire"
        kda = f"{p['kills']}/{p['deaths']}/{p['assists']}"
        text = f"{side} | {hero_name} | K/D/A: {kda}"

        y = 10 + idx * row_height
        icon = get_hero_icon(hero_name)

        if icon:
            img.paste(icon, (10, y))
        draw.text((80, y + 10), text, font=font, fill="white")

    stream = io.BytesIO()
    img.save(stream, format="PNG")
    stream.seek(0)

    await update.message.reply_photo(
        photo=stream, caption=f"🧾 Full Match Scoreboard\nMatch ID: {match_id}"
    )


handler = CommandHandler("scoreboard", scoreboard)
