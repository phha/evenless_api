from pydantic import BaseModel

from .sort_order import SortOrder


class Query(BaseModel):
    """A search query"""

    string: str = ""
    order: SortOrder = SortOrder.newest_first
    exclude_tags: list[str] = []
