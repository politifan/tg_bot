# tg_bot

Simple Telegram bot about a mini cafe.

## Features

- `/start` - greeting and inline menu.
- `/menu` - open the inline menu again.
- `/help` - show commands.
- Inline buttons: drink of the day, snack, about bot, close menu.

## Setup

1. Create a bot with BotFather and get a token.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set the token and run the bot.

PowerShell:

```powershell
$env:BOT_TOKEN="your_token"
python bot.py
```

cmd:

```bat
set BOT_TOKEN=your_token
python bot.py
```
