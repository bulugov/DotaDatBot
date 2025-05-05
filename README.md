# DotaDatBot 🎮

DotaDatBot is a Telegram bot that connects to the [OpenDota API](https://docs.opendota.com/) to fetch Dota 2 player data, recent match summaries, and display match scoreboards

## 🚀 Features

- 🔗 Link your Telegram account to your Dota 2 account
- 📊 View your latest match performance
- 🧾 Get a full vertical scoreboard with hero icons and K/D/A for all 10 players
- 📈 View your profile info: winrate, MMR estimate, and rank tier

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/bulugov/DotaDatBot.git
cd DotaDatBot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your bot

Create a `.env` file with your Telegram Bot token:

```env
BOT_TOKEN=your_telegram_bot_token
```

### 5. Run the bot

```bash
python bot.py
```

---

## 💡 Commands

| Command       | Description                                        |
| ------------- | -------------------------------------------------- |
| `/start`      | Welcome message                                    |
| `/link <id>`  | Link your Telegram to your Dota 2 account ID       |
| `/match`      | View your latest match performance                 |
| `/profile`    | See your MMR estimate, winrate, and rank           |
| `/scoreboard` | Get a visual scoreboard image of your latest match |

