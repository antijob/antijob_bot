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
    items: typing.Sequence[typing.Sequence[MenuItem]]

    @classmethod
    def init(cls, *items: typing.Sequence[MenuItem]):
        cls.items = items

    @classmethod
    def keyboard(cls, admin: bool = False) -> list[list[KeyboardButton | str]]:
        return [
            [item.button for item in row if not item.admin or admin]
            for row in cls.items
        ]

    @classmethod
    def reply_markup(
        cls,
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
            cls.keyboard(admin=admin),
            one_time_keyboard=one_time_keyboard,
            **kwargs,
        )

    @classmethod
    def _item_generator(cls) -> typing.Generator[MenuItem, None, None]:
        for row in cls.items:
            for item in row:
                yield item

    @classmethod
    def handlers(cls) -> list[MessageHandler]:
        return [item.handler for item in cls._item_generator() if item.handler]

    @classmethod
    def entry_point_handler(cls, conversation: Conversation) -> MessageHandler:
        for item in cls._item_generator():
            if item.enter == conversation:
                if item.handler:
                    return item.handler
                break
        raise Exception(f"handler for {conversation=} not found")
