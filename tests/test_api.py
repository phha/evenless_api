from .typing import ClientFactory


def test_root(make_client: ClientFactory) -> None:
    path = "/home/user/mail"
    version = 123

    class DB:
        def get_path(self) -> str:
            return path

        def get_version(self) -> int:
            return version

    client = make_client(DB())
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"database_version": version, "database_path": path}
