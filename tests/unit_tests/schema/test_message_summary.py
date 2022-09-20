from datetime import datetime
from unittest.mock import MagicMock, create_autospec

import notmuch as nm
import pytest

from evenless_api.schema.message_summary import MessageSummary


@pytest.fixture
def nm_message() -> MagicMock:
    mock = create_autospec(nm.Message, instance=True)
    mock.get_message_id.return_value = "id"
    mock.get_date.return_value = datetime.now()
    mock.get_header = lambda x: {
        "From": "foo@bar",
        "To": "bar@foo",
        "Subject": "Some Subject",
    }[x]
    mock.get_tags.return_value = ["tag1", "tag2", "tag3"]
    return mock


@pytest.fixture
def summary(nm_message: nm.Message) -> MessageSummary:
    return MessageSummary.from_notmuch(nm_message)


@pytest.mark.parametrize("attribute", ["message_id", "date", "tags"])
def test_attributes(
    nm_message: nm.Message, summary: MessageSummary, attribute: str
) -> None:
    assert getattr(summary, attribute) == getattr(nm_message, f"get_{attribute}")()


@pytest.mark.parametrize(
    "attribute,key", [("sender", "From"), ("recipient", "To"), ("subject", "Subject")]
)
def test_headers(
    nm_message: nm.Message, summary: MessageSummary, attribute: str, key: str
) -> None:
    assert getattr(summary, attribute) == nm_message.get_header(key)
