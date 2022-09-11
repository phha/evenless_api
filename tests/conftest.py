import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from evenless_api.main import app as evenless_app
from evenless_api.main import get_db

from .typing import ClientFactory


@pytest.fixture
def app() -> FastAPI:
    return evenless_app


@pytest.fixture
def make_client() -> ClientFactory:
    def inner(db=None) -> TestClient:
        def mock_get_db():
            if not db:
                raise ValueError("API function is calling get_db but no mock provided")
            return db

        evenless_app.dependency_overrides[get_db] = mock_get_db
        return TestClient(evenless_app)

    return inner
