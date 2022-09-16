from pydantic import BaseModel


class Info(BaseModel):
    """Configuration information"""

    database_path: str
    database_version: int
