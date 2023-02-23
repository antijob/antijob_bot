from telegram import Update
from telegram.ext import ConversationHandler

from antijob_bot.callbacks import broadcast
from antijob_bot.callbacks import feedback
from antijob_bot.callbacks import statistics
from antijob_bot.config import config
from antijob_bot.context import Context

__all__ = ("broadcast", "feedback", "statistics", "start")


async def start(update: Update, context: Context) -> int:
    if update.message.from_user.id not in context.user_ids:
        context.user_ids.add(update.message.from_user.id)
        with open(config.USERS_FILE, "a") as f:
            f.write(f"{update.message.from_user.id}\n")

    await update.message.reply_text(
        "Нажмите на кнопку в меню.",
        reply_markup=context.menu.reply_markup(update),
    )
    return ConversationHandler.END
