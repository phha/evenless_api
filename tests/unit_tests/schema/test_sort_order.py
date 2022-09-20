import pytest

from evenless_api.schema.sort_order import SortOrder

_names = ["oldest_first", "newest_first", "message_id", "unsorted"]


@pytest.mark.parametrize("name", _names)
def test_string_value(name: str) -> None:
    assert SortOrder[name] == name.upper()


@pytest.mark.parametrize("name, numeric_value", zip(_names, range(0, 3)))
def test_numeric_value(name: str, numeric_value: int):
    assert SortOrder[name].numeric_value == numeric_value
