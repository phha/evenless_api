from datetime import datetime
from typing import Callable, List
from unittest.mock import MagicMock

import pytest


def _mock_message(
    message_id: str = "id",
    date: datetime = datetime.now(),
    recipient: str = "bar@foo",
    sender: str = "foo@bar",
    subject: str = "Some Subject",
    filename: str = "some/file",
    tags: List[str] = ["tag1", "tag2", "tag3"],
) -> MagicMock:
    mock = MagicMock()
    mock.get_message_id.return_value = message_id
    mock.get_date.return_value = date
    mock.get_header = lambda x: {
        "From": sender,
        "To": recipient,
        "Subject": subject,
    }[x]
    mock.get_tags.return_value = tags
    mock.get_filename.return_value = filename
    return mock


@pytest.fixture
def mock_message() -> MagicMock:
    return _mock_message()


@pytest.fixture
def message_mocker() -> Callable[..., MagicMock]:
    return _mock_message
