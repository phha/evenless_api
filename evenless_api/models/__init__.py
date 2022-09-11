import email.policy

from datetime import datetime
from email import message_from_file
from email.message import EmailMessage
from enum import Enum
from typing import List, cast

import notmuch as nm

from pydantic import BaseModel


class Config(BaseModel):
    """Configuration information"""

    database_path: str
    database_version: int


class MessageSummary(BaseModel):
    """A Summary of an email message"""

    id: str
    date: datetime
    sender: str
    recipient: str
    subject: str
    tags: List[str]

    @classmethod
    def from_message(cls, message: nm.Message) -> "MessageSummary":
        """Create a summary from a notmuch Message object"""
        return cls(
            id=message.get_message_id(),
            date=message.get_date(),
            sender=message.get_header("From"),
            recipient=message.get_header("To"),
            subject=message.get_header("Subject"),
            tags=[t for t in message.get_tags()],
        )


class Message(MessageSummary):
    """An email message"""

    body: str

    @classmethod
    def from_message(cls, message: nm.Message) -> "Message":
        with open(message.get_filename(), "r") as fp:
            email_message = cast(
                EmailMessage,
                message_from_file(fp, _class=EmailMessage, policy=email.policy.default),
            )
            body = email_message.get_body()
            if body:
                return cls(
                    id=message.get_message_id(),
                    date=message.get_date(),
                    sender=message.get_header("From"),
                    recipient=message.get_header("To"),
                    subject=message.get_header("Subject"),
                    tags=[t for t in message.get_tags()],
                    body=body.get_payload(),
                )
            else:
                raise ValueError()


class SortOrder(str, Enum):
    """Sort order for search query"""

    oldest_first = "OLDEST_FIRST"
    newest_first = "NEWEST_FIRST"
    message_id = "MESSAGE_ID"
    unsorted = "UNSORTED"


class Query(BaseModel):
    """A search query"""

    string: str = ""
    order: SortOrder = SortOrder.newest_first
    exclude_tags: List[str] = []

    def prepare(self, db: nm.Database) -> nm.Query:
        """Prepare an executable query to the given database"""
        db_query = db.create_query(self.string)
        for tag in self.exclude_tags:
            db_query.exclude_tag(tag)
        db_query.set_sort(db_query.SORT.__getattribute__(self.order.value))
        return db_query
