import os

from typing import Generator, List

import notmuch as nm

from fastapi import Depends, FastAPI

from .models import Config, Message, MessageSummary, Query

app = FastAPI(title="EvenLess")


def get_db() -> Generator[nm.Database, None, None]:
    with nm.Database(os.environ["EVENLESS_DB_PATH"]) as db:
        yield db


@app.get("/", response_model=Config)
def get_root(db: nm.Database = Depends(get_db)) -> Config:
    """Get configuration information"""
    return Config(database_path=db.get_path(), database_version=db.get_version())


@app.get("/tags/")
def get_tags(db: nm.Database = Depends(get_db)) -> List[str]:
    """Get a list of all tags"""
    return [t for t in db.get_all_tags()]


@app.post("/search/messages", response_model=List[MessageSummary])
def search_messages(
    query: Query, db: nm.Database = Depends(get_db)
) -> List[MessageSummary]:
    """Query the database and return summaries of all matching messages"""
    q = query.prepare(db)
    messages = q.search_messages()
    return [MessageSummary.from_message(m) for m in messages]


@app.post("/message/", response_model=Message)
def get_message(id: str, db: nm.Database = Depends(get_db)) -> Message:
    return Message.from_message(db.find_message(id))
