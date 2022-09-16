from .message_summary import MessageSummary


class Message(MessageSummary):
    """An email message"""

    body: str
