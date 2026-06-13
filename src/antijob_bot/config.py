import os


class Config:
    def __getattr__(self, name: str) -> str:
        if value := os.getenv(name):
            return value

        # Support Docker/Kubernetes style secrets via VAR_FILE.
        if value_file := os.getenv(f"{name}_FILE"):
            with open(value_file, encoding="utf-8") as file:
                return file.read().strip()

        raise AttributeError(f"config has no option '{name}'")

    def get_admin_ids(self) -> set[int]:
        return set(map(int, self.ADMINS.split(",")))


config = Config()
