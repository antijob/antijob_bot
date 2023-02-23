from telegram.ext import CallbackContext
from telegram.ext import ExtBot

from antijob_bot.menu import Menu


class Context(CallbackContext[ExtBot, dict, dict, dict]):
    @property
    def menu(self) -> Menu:
        return self.bot_data["menu"]

    @property
    def user_ids(self) -> set[int]:
        return self.bot_data["user_ids"]
