from games.adapters.repository import RepositoryException, AbstractRepository
from games.domainmodel.model import User, Game, Review


def add_review_for_game(user: User, game: Game, rating: int, comment: str, repo: AbstractRepository) -> bool:
    """Adds a review for a specific game."""
    user = repo.get_user(str(user))

    if not user:
        raise ValueError("User not found in the repository.")

    review = Review(user, game, rating, comment)

    try:
        repo.add_review(review)
        return True
    except RepositoryException as e:
        return False


def get_reviews_for_game(game_id, repo: AbstractRepository) -> list:
    """Returns all reviews for a specific game."""
    return repo.get_reviews_for_game(game_id)


def calculate_average_rating(game_id, repo: AbstractRepository) -> float:
    """Calculate the average rating for a specific game."""
    reviews = get_reviews_for_game(game_id, repo)
    if reviews:
        total_rating = sum([review.rating for review in reviews])
        return total_rating / len(reviews)
    return 0  # Return 0 if no reviews yet


def reviews_per_user_limit(game_id, user_id, repo: AbstractRepository) -> int:
    """Ensure reviews per user is limited"""
    return repo.reviews_per_user_limit(game_id, user_id)
