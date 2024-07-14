from games.adapters.repository import AbstractRepository


def get_games(page, per_page, key, repo: AbstractRepository):
    return repo.get_games_by_key((page-1)*per_page, page*per_page, key)


def get_game_amount(repo: AbstractRepository):
    return repo.game_amount()


def get_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_games_by_genre(page, per_page, genre_name, repo: AbstractRepository):
    return repo.get_games_by_genre((page-1)*per_page, page*per_page, genre_name)


def get_game_amount_by_genre(genre_name, repo: AbstractRepository):
    return repo.get_game_amount_by_genre(genre_name)
