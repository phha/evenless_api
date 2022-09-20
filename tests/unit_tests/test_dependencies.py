from contextlib import suppress
from pathlib import Path
from unittest.mock import MagicMock, patch, sentinel

from evenless_api import dependencies
from evenless_api.settings import Settings


@patch(
    "evenless_api.dependencies.Settings", side_effect=[sentinel.first, sentinel.second]
)
def test_get_settings_cached(_) -> None:
    # given
    dependencies.get_settings.cache_clear()

    # when
    dependencies.get_settings()
    settings = dependencies.get_settings()

    # then
    assert settings is sentinel.first


@patch("notmuch.Database")
def test_get_db(mock_db) -> None:
    # given
    path = "db/path"
    settings = Settings(notmuch_db_path=path)

    # when
    gen = dependencies.get_db(settings=settings)
    next(gen)
    with suppress(StopIteration):
        next(gen)

    # then
    mock_db.assert_called_once_with(path)
    mock_db.return_value.__enter__.assert_called_once()
    mock_db.return_value.__exit__.assert_called_once()


@patch("evenless_api.dependencies.message_from_file")
def test_get_message_body(mock) -> None:
    # given
    inner = dependencies.get_message_body()
    mock_path = MagicMock(spec=Path)
    body = "This is an email body."
    mock.return_value.get_body.return_value.get_payload.return_value = body

    # when
    result = inner(mock_path)

    # then
    mock_path.open.assert_called_once()
    assert result == body
