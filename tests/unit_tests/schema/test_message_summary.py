import notmuch as nm
import pytest

from evenless_api.schema.message_summary import MessageSummary


@pytest.fixture
def summary(mock_message: nm.Message) -> MessageSummary:
    return MessageSummary.from_notmuch(mock_message)


@pytest.mark.parametrize("attribute", ["message_id", "date", "tags"])
def test_attributes(
    mock_message: nm.Message, summary: MessageSummary, attribute: str
) -> None:
    assert getattr(summary, attribute) == getattr(mock_message, f"get_{attribute}")()


@pytest.mark.parametrize(
    "attribute,key", [("sender", "From"), ("recipient", "To"), ("subject", "Subject")]
)
def test_headers(
    mock_message: nm.Message, summary: MessageSummary, attribute: str, key: str
) -> None:
    assert getattr(summary, attribute) == mock_message.get_header(key)
