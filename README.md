# HardAliTelegramBot
# HardAliTelegramBot

This is a simple template for an online tutor Telegram bot built with **aiogram 3**.

## Features

- Student registration via `/start`.
- Admin commands to list students and send assignments.
- Students can submit homework for specific assignments.
- Async SQLAlchemy with SQLite database.

## Quick start

1. Install requirements:
   ```bash
   pip install aiogram sqlalchemy aiosqlite
   ```
2. Set environment variables `BOT_TOKEN` and optional `ADMIN_IDS` (comma separated Telegram IDs).
3. Run bot:
   ```bash
   python -m bot.app
   ```