from enum import Enum


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
