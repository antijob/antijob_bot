import redis.asyncio as redis
from telegram.ext import DictPersistence
from telegram.ext._utils.types import ConversationDict
from telegram.ext._utils.types import ConversationKey

from antijob_bot.config import config

client: redis.Redis = redis.Redis(
    host=config.DB_HOST,
    port=int(config.DB_PORT),
    password=config.DB_PASSWORD,
    decode_responses=True,
)


class RedisPersistence(DictPersistence):
    CONVERSATIONS_KEY = "conversations"

    async def get_conversations(self, name: str) -> ConversationDict:
        if self.conversations is None:
            if json_string := await client.get(self.CONVERSATIONS_KEY):
                self._conversations = self._decode_conversations_from_json(json_string)
                self._conversations_json = json_string
            else:
                self._conversations = {}
                self._conversations_json = None
        return await super().get_conversations(name)

    async def update_conversation(
        self, name: str, key: ConversationKey, new_state: object | None
    ) -> None:
        await super().update_conversation(name, key, new_state)
        await self.flush()

    async def flush(self) -> None:
        if self._conversations_json or self._conversations:
            await client.set(self.CONVERSATIONS_KEY, self.conversations_json)


class UserStore:
    KEY = "users"

    @classmethod
    async def add(cls, user_id: int) -> int:
        return await client.sadd(cls.KEY, user_id)

    @classmethod
    async def count(cls) -> int:
        return await client.scard(cls.KEY)


class BroadcastStore:
    def __init__(self, message_id: int):
        self.KEY = f"broadcast:{message_id}"

    async def add(self, user_id: int) -> int:
        return await client.sadd(self.KEY, user_id)

    async def count(self) -> int:
        return await client.scard(self.KEY)

    async def ids(self) -> set[bytes | float | int | str]:
        return await client.sdiff(UserStore.KEY, self.KEY)
