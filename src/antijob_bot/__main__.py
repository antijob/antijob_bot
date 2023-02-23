from telegram import KeyboardButton
from telegram import WebAppInfo
from telegram.ext import ApplicationBuilder
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

from antijob_bot import callbacks
from antijob_bot import conversations
from antijob_bot.config import config
from antijob_bot.context import Context
from antijob_bot.menu import Menu
from antijob_bot.menu import MenuItem

menu = Menu(
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
    ApplicationBuilder()
    .token(config.TOKEN)
    .context_types(ContextTypes(context=Context))
    .build()
)

application.bot_data["menu"] = menu
application.bot_data["user_ids"] = config.get_user_ids()

start_handler = CommandHandler("start", callbacks.start)
feedback_handler = ConversationHandler(
    entry_points=[menu.entry_point_handler(conversations.Conversation.FEEDBACK)],
    states={
        conversations.EXPECT_MESSAGE: [
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
)
broadcast_handler = ConversationHandler(
    entry_points=[menu.entry_point_handler(conversations.Conversation.BROADCAST)],
    states={
        conversations.EXPECT_MESSAGE: [
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
)

application.add_handler(start_handler)
application.add_handler(feedback_handler)
application.add_handler(broadcast_handler)
application.add_handlers(menu.handlers())  # type: ignore [arg-type]
application.add_handler(MessageHandler(filters.ALL, callbacks.start))


if __name__ == "__main__":
    application.run_polling()
