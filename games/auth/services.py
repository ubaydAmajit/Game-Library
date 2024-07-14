from werkzeug.security import generate_password_hash, check_password_hash
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NonUniqueUsernameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def new_user(username: str, password: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is not None:
        raise NonUniqueUsernameException
    pwd_hash = generate_password_hash(password)
    repo.add_user(User(username, pwd_hash))


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def user_to_dict(user: User):
    return {"username": user.username_for_ui, "password": user.password}


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None or not check_password_hash(user.password, password):
        raise AuthenticationException
