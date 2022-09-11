from typing import Callable

from fastapi.testclient import TestClient

ClientFactory = Callable[..., TestClient]
