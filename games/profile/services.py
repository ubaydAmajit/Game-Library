from games.adapters.repository import AbstractRepository


def get_username(username, repo: AbstractRepository):
    user = repo.get_user(username)
    return user


def get_reviews_by_user(user_id, repo: AbstractRepository):
    reviews = repo.get_reviews_by_user(user_id)
    return reviews

