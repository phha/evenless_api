import pytest

from evenless_api.settings import Settings


@pytest.fixture
def db_path() -> str:
    return "db/path"


def test_settings_defaults() -> None:
    # when
    settings = Settings()

    # then
    assert settings.notmuch_db_path is None


def test_settings_from_env(db_path: str, monkeypatch: pytest.MonkeyPatch) -> None:
    # given
    monkeypatch.setenv("NOTMUCH_DB_PATH", db_path)

    # when
    settings = Settings()

    # then
    assert settings.notmuch_db_path == db_path
