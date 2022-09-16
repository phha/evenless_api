from datetime import datetime

import notmuch as nm

from pydantic import BaseModel


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
