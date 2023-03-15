import os


class Config:
    def __getattr__(self, name: str) -> str:
        if (value := os.getenv(name)) is None:
            raise AttributeError(f"config has no option '{name}'")
        return value

    def get_admin_ids(self) -> set[int]:
        return set(map(int, self.ADMINS.split(",")))


config = Config()
