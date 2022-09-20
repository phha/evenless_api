from evenless_api.main import app


def test_app_title() -> None:
    assert app.title == "Evenless"
