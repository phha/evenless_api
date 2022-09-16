import email.policy
import os

from collections.abc import Generator
from email import message_from_file
from email.message import EmailMessage
from typing import Callable, cast

import notmuch as nm


def get_db() -> Generator[nm.Database, None, None]:
    with nm.Database(os.environ["EVENLESS_DB_PATH"]) as db:
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
