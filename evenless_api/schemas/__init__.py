from datetime import datetime
from enum import Enum

import notmuch as nm

from pydantic import BaseModel


class Info(BaseModel):
    """Configuration information"""

    database_path: str
    database_version: int


class MessageSummary(BaseModel):
    """A Summary of an email message"""

    message_id: str
    date: datetime
    sender: str
    recipient: str
    subject: str
    tags: list[str]

    @classmethod
    def from_notmuch(cls, message: nm.Message) -> "MessageSummary":
        """Create a summary from a notmuch Message object"""
        return cls(
            message_id=message.get_message_id(),
            date=message.get_date(),
            sender=message.get_header("From"),
            recipient=message.get_header("To"),
            subject=message.get_header("Subject"),
            tags=[t for t in message.get_tags()],
        )


class Message(MessageSummary):
    """An email message"""

    body: str


class SortOrder(str, Enum):
    """Sort order for search query"""

    oldest_first = "OLDEST_FIRST"
    newest_first = "NEWEST_FIRST"
    message_id = "MESSAGE_ID"
    unsorted = "UNSORTED"

    @property
    def numeric_value(self) -> int:
        return {
            SortOrder.oldest_first: 0,
            SortOrder.newest_first: 1,
            SortOrder.message_id: 2,
            SortOrder.unsorted: 3,
        }[self]


class Query(BaseModel):
    """A search query"""

    string: str = ""
    order: SortOrder = SortOrder.newest_first
    exclude_tags: list[str] = []
