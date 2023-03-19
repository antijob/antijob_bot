from telegram import Bot
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Message
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

from antijob_bot import conversations
from antijob_bot.database import BroadcastStore
from antijob_bot.database import UserStore
from antijob_bot.logging import logger
from antijob_bot.menu import Menu


async def broadcast(message: Message, bot: Bot) -> None:
    store = BroadcastStore(message.id)
    for user_id in await store.ids():
        chat_id = int(user_id)
        try:
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.id,
            )
        except Exception as e:
            logger.error(f"couldn't send a message to {chat_id}", exc_info=e)
        else:
            await store.add(chat_id)
    await message.reply_text(
        "Рассылка завершена. Отправлено сообщений:"
        f" {await store.count()} из {await UserStore.count()}."
    )


async def enter_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> object:
    if update.message.reply_to_message:
        await update.message.reply_text("Рассылка продолжается.")
        await broadcast(update.message.reply_to_message, context.bot)
        return ConversationHandler.END

    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            "Отмена", callback_data=conversations.CANCEL_BROADCAST_DATA
        )
    )
    await update.message.reply_text(
        "Отправьте сообщение для рассылки.", reply_markup=reply_markup
    )
    return conversations.Conversation.EXPECT_MESSAGE


async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Рассылка начинается.")
    await broadcast(update.message, context.bot)
    return ConversationHandler.END


async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await context.bot.send_message(
        update.callback_query.from_user.id,
        "Рассылка отменена.",
        reply_markup=Menu.reply_markup(update),
    )
    return ConversationHandler.END
