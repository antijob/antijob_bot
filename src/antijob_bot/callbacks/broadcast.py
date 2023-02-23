from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ConversationHandler

from antijob_bot import conversations
from antijob_bot.context import Context
from antijob_bot.logging import logger


async def enter_broadcast(update: Update, context: Context) -> object:
    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            "Отмена", callback_data=conversations.CANCEL_BROADCAST_DATA
        )
    )
    await update.message.reply_text(
        "Отправьте сообщение для рассылки.", reply_markup=reply_markup
    )
    return conversations.EXPECT_MESSAGE


async def send_broadcast(update: Update, context: Context) -> int:
    sent_messages = 0
    for user_id in context.user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=update.message.text)
            sent_messages += 1
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение для {user_id}.", exc_info=e)
    await update.message.reply_text(
        "Рассылка завершена. Отправлено сообщений:"
        f" {sent_messages} из {len(context.user_ids)}."
    )
    return ConversationHandler.END


async def cancel_broadcast(update: Update, context: Context) -> int:
    await update.callback_query.answer()
    await context.bot.send_message(
        update.callback_query.from_user.id,
        "Рассылка отменена.",
        reply_markup=context.menu.reply_markup(update),
    )
    return ConversationHandler.END
