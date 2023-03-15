from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Message
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

from antijob_bot import conversations
from antijob_bot.callbacks.start import start
from antijob_bot.config import config
from antijob_bot.database import client
from antijob_bot.menu import Menu


def feedback_key(chat_id: int, message_id: int) -> str:
    return f"feedback:{chat_id}:{message_id}"


async def set_feedback_value(chat_id: int, message_id: int, original: Message) -> None:
    value = f"{original.chat.id} {original.id}"
    await client.set(feedback_key(chat_id, message_id), value)


async def enter_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> object:
    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Отмена", callback_data=conversations.CANCEL_FEEDBACK_DATA)
    )
    await update.message.reply_text("Напишите сообщение.", reply_markup=reply_markup)
    return conversations.EXPECT_MESSAGE


async def send_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    copy = await update.message.forward(config.FEEDBACK_CHAT_ID)
    await set_feedback_value(copy.chat.id, copy.id, update.message)
    await update.message.reply_text("Сообщение отправлено.")
    return ConversationHandler.END


async def cancel_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await context.bot.send_message(
        update.callback_query.from_user.id,
        "Отправка отменена.",
        reply_markup=Menu.reply_markup(update),
    )
    return ConversationHandler.END


async def continue_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rtm = update.message.reply_to_message
    if (
        rtm.from_user.id != context.bot.id
        or (value := await client.get(feedback_key(rtm.chat.id, rtm.id))) is None
    ):
        return await start(update, context)

    chat_id, message_id = value.split()
    copy = await update.message.copy(chat_id, reply_to_message_id=message_id)
    await set_feedback_value(chat_id, copy.message_id, update.message)
    await update.message.reply_text("Ответ отправлен.")
