import dataclasses
import functools
import typing

from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import MessageHandler
from telegram.ext import filters
from telegram.ext._utils.types import HandlerCallback

from antijob_bot.config import config
from antijob_bot.conversations import Conversation


@dataclasses.dataclass
class MenuItem:
    button: KeyboardButton | str
    callback: HandlerCallback | None = None
    _: dataclasses.KW_ONLY
    enter: Conversation | None = None
    admin: bool = False

    @property
    def text(self) -> str:
        if isinstance(self.button, KeyboardButton):
            return self.button.text
        else:
            return self.button

    @functools.cached_property
    def filters(self) -> filters.BaseFilter:
        result: filters.BaseFilter = filters.Text([self.text])
        if self.admin:
            result &= filters.User(config.get_admin_ids())
        return result

    @functools.cached_property
    def handler(self) -> MessageHandler | None:
        return MessageHandler(self.filters, self.callback) if self.callback else None


class Menu:
    def __init__(self, *items: typing.Sequence[MenuItem]):
        self.items = items

    def keyboard(self, admin: bool = False) -> list[list[KeyboardButton | str]]:
        return [
            [item.button for item in row if not item.admin or admin]
            for row in self.items
        ]

    def reply_markup(
        self,
        update: Update | None = None,
        *,
        one_time_keyboard: bool = True,
        **kwargs,
    ) -> ReplyKeyboardMarkup:
        if update and update.effective_user:
            admin = update.effective_user.id in config.get_admin_ids()
        else:
            admin = False
        return ReplyKeyboardMarkup(
            self.keyboard(admin=admin),
            one_time_keyboard=one_time_keyboard,
            **kwargs,
        )

    def _item_generator(self) -> typing.Generator[MenuItem, None, None]:
        for row in self.items:
            for item in row:
                yield item

    def handlers(self) -> list[MessageHandler]:
        return [item.handler for item in self._item_generator() if item.handler]

    def entry_point_handler(self, conversation: Conversation) -> MessageHandler:
        for item in self._item_generator():
            if item.enter == conversation:
                if item.handler:
                    return item.handler
                break
        raise Exception(f"handler for {conversation=} not found")
