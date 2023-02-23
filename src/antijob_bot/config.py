import os

from antijob_bot.logging import logger


class Config:
    def __getattr__(self, name: str) -> str:
        if (value := os.getenv(name)) is None:
            raise AttributeError(f"config has no option '{name}'")
        return value

    def get_admin_ids(self) -> set[int]:
        return set(map(int, self.ADMINS.split(",")))

    def get_user_ids(self) -> set[int]:
        try:
            with open(self.USERS_FILE, "r") as f:
                return set(map(int, f.read().splitlines()))
        except FileNotFoundError:
            logger.warning("file does not exist, using empty user set")
            return set()


config = Config()
