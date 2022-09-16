from pydantic import BaseSettings


class Settings(BaseSettings):
    notmuch_db_path: str | None = None
