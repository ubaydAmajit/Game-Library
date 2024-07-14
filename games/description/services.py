from games.adapters.repository import AbstractRepository


def get_game(game_id, repo: AbstractRepository):
    return repo.get_game(game_id)
