import pytest
from flask import Flask

from games import create_app
from games.adapters import memory_repository


@pytest.fixture
def in_memory_repo():
    repo = memory_repository.MemoryRepository()
    memory_repository.populate("./games/adapters/data/games.csv", repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()


class ClientAuth:
    def __init__(self, client: Flask):
        self.client = client

    def register(self, username="DJ_HyperFresh", password="**7Zr!g^XMh%r3"):
        return self.client.post("auth/register", data={"username": username, "password": password})

    def login(self, username="DJ_HyperFresh", password="**7Zr!g^XMh%r3"):
        return self.client.post("auth/login", data={"username": username, "password": password})

    def logout(self):
        return self.client.get("auth/logout")


@pytest.fixture
def auth(client):
    return ClientAuth(client)
