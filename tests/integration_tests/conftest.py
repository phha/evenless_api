from unittest.mock import Mock

import notmuch as nm
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from evenless_api import dependencies
from evenless_api.main import app as evenless_app

from . import Overrides


@pytest.fixture
def app(overrides: Overrides) -> FastAPI:
    evenless_app.dependency_overrides = overrides
    return evenless_app


@pytest.fixture
def overrides() -> Overrides:
    return Overrides()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_db(overrides: Overrides) -> Mock:
    return overrides.mock(dependencies.get_db, nm.Database)
