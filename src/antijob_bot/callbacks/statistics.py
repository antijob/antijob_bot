from telegram import Update

from antijob_bot.context import Context


async def show_statistics(update: Update, context: Context) -> None:
    user_count = len(context.user_ids)
    await update.message.reply_text(
        f"Количество пользователей: {user_count}.",
        reply_markup=context.menu.reply_markup(update),
    )
