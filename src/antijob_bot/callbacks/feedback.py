from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ConversationHandler

from antijob_bot import conversations
from antijob_bot.config import config
from antijob_bot.context import Context


async def enter_feedback(update: Update, context: Context) -> object:
    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Отмена", callback_data=conversations.CANCEL_FEEDBACK_DATA)
    )
    await update.message.reply_text("Напишите сообщение.", reply_markup=reply_markup)
    return conversations.EXPECT_MESSAGE


async def send_feedback(update: Update, context: Context) -> int:
    await update.message.forward(config.FEEDBACK_CHAT_ID)
    await update.message.reply_text("Сообщение отправлено.")
    return ConversationHandler.END


async def cancel_feedback(update: Update, context: Context) -> int:
    await update.callback_query.answer()
    await context.bot.send_message(
        update.callback_query.from_user.id,
        "Отправка отменена.",
        reply_markup=context.menu.reply_markup(update),
    )
    return ConversationHandler.END
