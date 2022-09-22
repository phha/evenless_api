from datetime import datetime
from typing import Callable, Iterable
from unittest.mock import MagicMock, Mock, call

from fastapi.testclient import TestClient

from evenless_api import dependencies
from evenless_api.schema import Message, MessageSummary, SortOrder

from . import Overrides


def test_get_root(client: TestClient, mock_db: Mock) -> None:
    # given
    path = "/home/user/mail"
    version = 123
    mock_db.get_path.return_value = path
    mock_db.get_version.return_value = version

    # when
    response = client.get("/")

    # then
    assert response.status_code == 200
    assert response.json() == {"database_version": version, "database_path": path}
    mock_db.get_path.assert_called_once()
    mock_db.get_version.assert_called_once()


def test_get_tags(client: TestClient, mock_db: Mock) -> None:
    # given
    tags = ["tag1", "tag2", "tag3"]
    mock_db.get_all_tags.return_value = tags

    # when
    response = client.get("/tags/")

    # then
    assert response.status_code == 200
    assert response.json() == tags
    mock_db.get_all_tags.assert_called_once()


def test_search_messages(
    client: TestClient, mock_db: Mock, message_mocker: Callable[..., MagicMock]
) -> None:
    # given
    order = SortOrder.oldest_first
    body_json = {"string": "FooBar", "exclude_tags": ["foo"], "order": order.value}
    messages: Iterable[MessageSummary] = []
    for i in range(0, 3):
        msg = MessageSummary(
            message_id=f"id{i}",
            date=datetime.now(),
            sender=f"sender{i}@expample.com",
            recipient=f"recipient{i}@example.com",
            tags=[f"tag{i}", f"tag1{i}", f"tag2{i}", "common"],
            subject="Subject {i}",
        )
        messages.append(msg)
    notmuch_messages = [message_mocker(**m.dict()) for m in messages]
    mock_query = mock_db.create_query.return_value
    mock_query.search_messages.return_value = notmuch_messages
    expected_tags = [call(t) for t in body_json["exclude_tags"]]

    # when
    response = client.post("/search/messages/", json=body_json)

    # then
    assert response.status_code == 200
    for jsonmsg, msg in zip(response.json(), messages):
        assert MessageSummary.parse_obj(jsonmsg) == msg
    assert expected_tags == mock_query.exclude_tag.mock_calls
    mock_db.create_query.assert_called_once_with(body_json["string"])
    mock_query.set_sort.assert_called_once_with(order.numeric_value)


def test_get_message(
    client: TestClient, overrides: Overrides, mock_db: Mock, mock_message
) -> None:
    # given
    body = "Message Body"
    mock_db.find_message.return_value = mock_message
    mock_get_email_body = overrides.mock(
        dependencies.get_message_body, Callable[[str], str]
    )
    mock_get_email_body.return_value = body

    # when
    response = client.post(f"/message/?message_id={mock_message.get_message_id()}")
    message = Message.parse_obj(response.json())

    # then
    assert response.status_code == 200
    assert message.body == body
    assert message.message_id == mock_message.get_message_id()
    assert message.date == mock_message.get_date()
    assert message.tags == mock_message.get_tags()
    mock_db.find_message.assert_called_once_with(mock_message.get_message_id())
    mock_get_email_body.assert_called_once_with(mock_message.get_filename())
