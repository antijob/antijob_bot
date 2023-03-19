from warnings import filterwarnings

from ptbcontrib.reply_to_message_filter import ReplyToMessageFilter
from telegram import KeyboardButton
from telegram import WebAppInfo
from telegram.ext import ApplicationBuilder
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import filters
from telegram.warnings import PTBUserWarning

from antijob_bot import callbacks
from antijob_bot import conversations
from antijob_bot.config import config
from antijob_bot.database import RedisPersistence
from antijob_bot.menu import Menu
from antijob_bot.menu import MenuItem

Menu.init(
    [
        MenuItem(KeyboardButton("Сайт", web_app=WebAppInfo(url=config.MAIN_URL))),
        MenuItem(KeyboardButton("Новости", web_app=WebAppInfo(url=config.NEWS_URL))),
    ],
    [
        MenuItem(
            KeyboardButton("Написать"),
            callbacks.feedback.enter_feedback,
            enter=conversations.Conversation.FEEDBACK,
        )
    ],
    [
        MenuItem(
            KeyboardButton("Рассылка"),
            callbacks.broadcast.enter_broadcast,
            enter=conversations.Conversation.BROADCAST,
            admin=True,
        )
    ],
    [
        MenuItem(
            KeyboardButton("Статистика"),
            callbacks.statistics.show_statistics,
            admin=True,
        )
    ],
)

application = (
    ApplicationBuilder().token(config.TOKEN).persistence(RedisPersistence()).build()
)

filterwarnings("ignore", r".*CallbackQueryHandler", PTBUserWarning)

start_handler = CommandHandler("start", callbacks.start.start)
feedback_handler = ConversationHandler(
    entry_points=[Menu.entry_point_handler(conversations.Conversation.FEEDBACK)],
    states={
        conversations.Conversation.EXPECT_MESSAGE: [
            MessageHandler(filters.ALL, callbacks.feedback.send_feedback)
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            callbacks.feedback.cancel_feedback,
            pattern=conversations.CANCEL_FEEDBACK_DATA,
        ),
        start_handler,
    ],
    name="feedback",
    persistent=True,
)
broadcast_handler = ConversationHandler(
    entry_points=[Menu.entry_point_handler(conversations.Conversation.BROADCAST)],
    states={
        conversations.Conversation.EXPECT_MESSAGE: [
            MessageHandler(filters.ALL, callbacks.broadcast.send_broadcast)
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            callbacks.broadcast.cancel_broadcast,
            pattern=conversations.CANCEL_BROADCAST_DATA,
        ),
        start_handler,
    ],
    name="broadcast",
    persistent=True,
)
continue_feedback_handler = MessageHandler(
    ReplyToMessageFilter(filters.ALL),
    callbacks.feedback.continue_feedback,
)

application.add_handler(start_handler)
application.add_handler(feedback_handler)
application.add_handler(broadcast_handler)
application.add_handlers(Menu.handlers())  # type: ignore [arg-type]
application.add_handler(continue_feedback_handler)
application.add_handler(MessageHandler(filters.ALL, callbacks.start.start))

if __name__ == "__main__":
    application.run_polling()
