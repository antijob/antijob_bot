from telegram import Update
from telegram.ext import ContextTypes

from antijob_bot.database import UserStore
from antijob_bot.menu import Menu


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_count = await UserStore.count()
    await update.message.reply_text(
        f"Количество пользователей: {user_count}.",
        reply_markup=Menu.reply_markup(update),
    )
