import notmuch as nm

from fastapi import Depends, FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from evenless_api import dependencies

from .schemas import Info, Message, MessageSummary, Query

app = FastAPI(title="EvenLess")
app.add_middleware(GZipMiddleware)


@app.get("/", response_model=Info)
def get_root(db: nm.Database = Depends(dependencies.get_db)) -> Info:
    """Get configuration information"""
    return Info(database_path=db.get_path(), database_version=db.get_version())


@app.get("/tags/")
def get_tags(db: nm.Database = Depends(dependencies.get_db)) -> list[str]:
    """Get a list of all tags"""
    return [t for t in db.get_all_tags()]


@app.post("/search/messages/", response_model=list[MessageSummary])
def search_messages(
    query: Query, db: nm.Database = Depends(dependencies.get_db)
) -> list[MessageSummary]:
    """Query the database and return summaries of all matching messages"""
    db_query = db.create_query(query.string)
    for tag in query.exclude_tags:
        db_query.exclude_tag(tag)
    db_query.set_sort(query.order.numeric_value)
    messages = db_query.search_messages()
    return [MessageSummary.from_notmuch(m) for m in messages]


@app.post("/message/", response_model=Message)
def get_message(
    message_id: str,
    db: nm.Database = Depends(dependencies.get_db),
    get_message_body=Depends(dependencies.get_message_body),
) -> Message:
    notmuch_message = db.find_message(message_id)
    body = get_message_body(notmuch_message.get_filename())
    return Message(**MessageSummary.from_notmuch(notmuch_message).dict(), body=body)
