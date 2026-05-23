import logging
import os
import random

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
load_dotenv()

DRINKS = [
    ("Espresso", "A short and strong coffee for a quick reset."),
    ("Cappuccino", "Soft coffee with milk foam."),
    ("Latte", "A calm drink for a long chat."),
    ("Cocoa", "Sweet, warm, and caffeine-free."),
]

SNACKS = [
    "croissant",
    "cheesecake",
    "brownie",
    "lemon tart",
]


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Drink of the day", callback_data="drink"),
                InlineKeyboardButton("Snack", callback_data="snack"),
            ],
            [
                InlineKeyboardButton("About bot", callback_data="about"),
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name if update.effective_user else "guest"
    text = (
        f"Hi, {user_name}!\n\n"
        "I am a simple mini cafe bot. Open the menu and choose an option."
    )
    await update.message.reply_text(text, reply_markup=main_keyboard())


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Mini cafe menu:", reply_markup=main_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "<b>Commands</b>\n"
        "/start - start the bot\n"
        "/menu - open the inline menu\n"
        "/help - show this help"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def handle_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "drink":
        name, description = random.choice(DRINKS)
        await query.edit_message_text(
            f"<b>{name}</b>\n{description}",
            parse_mode=ParseMode.HTML,
            reply_markup=main_keyboard(),
        )
        return

    if query.data == "snack":
        snack = random.choice(SNACKS)
        await query.edit_message_text(
            f"Today you may like: <b>{snack}</b>.",
            parse_mode=ParseMode.HTML,
            reply_markup=main_keyboard(),
        )
        return

    if query.data == "about":
        await query.edit_message_text(
            "This is a small Telegram bot with one inline menu, buttons, and commands.",
            reply_markup=main_keyboard(),
        )
        return

    if query.data == "close":
        await query.edit_message_text("Menu closed. Use /menu to open it again.")


def build_app() -> Application:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Set BOT_TOKEN environment variable before starting the bot.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_menu_click))
    return app


def main() -> None:
    app = build_app()
    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
