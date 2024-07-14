import pytest
from flask import request, url_for, session


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200


@pytest.mark.parametrize(("page", "order", "result"), ((0, "Newest", b"No Games found at specified page"),
                                                       (75, "Newest", b"No Games found at specified page"),
                                                       (1, "Newest", b"Deer Journey"), (1, "Oldest", b"Xpand Rally")))
def test_library_pages(client, page, order, result):
    response = client.get("/games", query_string={"page": page, "sortBy": order})
    assert result in response.data


@pytest.mark.parametrize(("term", "key", "result"), (("super meat boy", "title", b"Super Meat Boy"),
                                                     ("a Franco-Spanish painter and a key figure in the pictorial",
                                                      "description", b"Maria Blanchard Virtual Gallery"),
                                                     ("Pablo Picazo", "publisher", b"Deer Journey"),
                                                     ("sdjfjlkgkbhsdjghlj", "title",
                                                      b"No Games Found With The Specified Criteria")))
def test_search(client, term, key, result):
    response = client.get("/search", query_string={"term": term, "key": key})
    assert result in response.data


def test_account_creation(client):
    # Test that the page can be retrieved
    assert client.get("/auth/register").status_code == 200

    # Check that multiple users can be successfully registered
    response = client.post("/auth/register", data={"username": "DJ_HyperFresh", "password": "**7Zr!g^XMh%r3"},
                           follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == '/auth/login'

    response = client.post("/auth/register", data={"username": "MC_Princess", "password": "**7Zr!g^XMh%r3"},
                           follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == '/auth/login'


@pytest.mark.parametrize(("username", "password", "message"),
                         (("Ad", "**7Zr!g^XMh%r3", b"Your Username needs to be longer"),
                          ("", "**7Zr!g^XMh%r3", b"Please enter your Username"),
                          ("DJ_HyperFresh", "", b"Your password is required"),
                          ("DJ_HyperFresh", "**7Zr!g^XMh% r3",
                           b"Your password should contain lowercase and uppercase letters, numbers, and no spaces"),
                          ("DJ_HyperFresh", "**7zr!g^xmh%r3",
                           b"Your password should contain lowercase and uppercase letters, numbers, and no spaces"),
                          ("DJ_HyperFresh", "**7ZR!G^XMH%R3",
                           b"Your password should contain lowercase and uppercase letters, numbers, and no spaces"),
                          ("DJ_HyperFresh", "**TZr!g^XMh%rE",
                           b"Your password should contain lowercase and uppercase letters, numbers, and no spaces"),
                          ("DJ_HyperFresh", "**7Zr!g^X", b"Your password should contain at least 10 characters")))
def test_input_validation(username, password, message, client):
    response = client.post("/auth/register", data={"username": username, "password": password})
    assert message in response.data


def test_existing_user(client):
    # register user
    client.post("/auth/register", data={"username": "DJ_HyperFresh", "password": "**7Zr!g^XMh%r3"})
    # try register user second time with same capitalization
    response = client.post("/auth/register", data={"username": "DJ_HyperFresh", "password": "**7Zr!g^XMh%r3"})
    assert b"This Username Is Already Taken" in response.data
    # try register user again with different capitalization
    response = client.post("/auth/register", data={"username": "DJ_hyperfresh", "password": "**7Zr!g^XMh%r3"})
    assert b"This Username Is Already Taken" in response.data


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200

    auth.register()
    response = client.post("auth/login", data={"username": "DJ_HyperFresh", "password": "**7Zr!g^XMh%r3"},
                           follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == '/'

    with client:
        client.get("/")
        assert session["username"] == "DJ_HyperFresh"


def test_logout(client, auth):
    auth.register()
    auth.login()

    with client:
        auth.logout()
        assert "username" not in session


def test_description(client, auth):
    auth.register()
    auth.login()

    response = client.get("/description/2010700")
    assert response.status_code == 200


def test_reviews(client, auth, in_memory_repo):
    auth.register()
    auth.login()

    print(in_memory_repo.get_game(2010700))

    response = client.get("write_review/2010700")
    assert response.status_code == 200
    response = client.post(
        "write_review/2010700",
        data={"rating": 5, "comment": "Test Comment String"},
        follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == '/game_description/2010700'


def test_review_invalid_input(client, auth):
    auth.register()
    auth.login()

    response = client.post("/write_review/2010700", data={
        "rating": 5,
        "comment": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vitae tellus orci. Vestibulum "
                   "faucibus molestie sodales. Donec semper felis quis magna ultrices fringilla. Duis consequat "
                   "ornare nisi, tempor gravida nunc molestie at. Duis fermentum dapibus erat, sit amet feugiat lorem "
                   "accumsan ac. Vivamus enim eros, efficitur in convallis sed, tempor auctor turpis. Etiam id "
                   "euismod arcu, quis ultrices lacus. Cras mattis eleifend eros nec auctor. Nunc consectetur enim "
                   "diam, ac lacinia velit eleifend quis amet. "})

    assert b"Your Review Should Be Between 1 to 500 Characters" in response.data
