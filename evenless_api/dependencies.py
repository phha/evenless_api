import email.policy

from collections.abc import Generator
from email import message_from_file
from email.message import EmailMessage
from functools import lru_cache
from typing import Callable, cast

import notmuch as nm

from fastapi import Depends

from evenless_api.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_db(
    settings: Settings = Depends(get_settings),
) -> Generator[nm.Database, None, None]:
    with nm.Database(settings.notmuch_db_path) as db:
        yield db


def get_message_body() -> Callable[[str], str | None]:
    def inner(filename: str) -> str | None:
        with open(filename, "r") as fp:
            email_message = cast(
                EmailMessage,
                message_from_file(fp, _class=EmailMessage, policy=email.policy.default),
            )
            body = email_message.get_body()
            if body:
                return body.get_payload()

    return inner
