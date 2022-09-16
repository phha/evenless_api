from datetime import datetime
from typing import Iterable

from evenless_api.schemas import MessageSummary


class MockMessage(MessageSummary):
    filename: str | None = None
    body: str | None = None

    def get_message_id(self) -> str:
        return self.message_id

    def get_date(self) -> datetime:
        return self.date

    def get_tags(self) -> Iterable[str]:
        return self.tags

    def get_filename(self) -> str | None:
        return self.filename

    def get_header(self, key: str) -> str:
        return {"From": self.sender, "To": self.recipient, "Subject": self.subject}[key]
