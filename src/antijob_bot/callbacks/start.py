from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

from antijob_bot.database import UserStore
from antijob_bot.menu import Menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await UserStore.add(update.message.from_user.id)
    await update.message.reply_text(
        "Нажмите на кнопку в меню.",
        reply_markup=Menu.reply_markup(update),
    )
    return ConversationHandler.END
