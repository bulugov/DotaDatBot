from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from handlers import match, link, profile, scoreboard

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(match.handler)
app.add_handler(link.handler)
app.add_handler(profile.handler)
app.add_handler(scoreboard.handler)

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()

