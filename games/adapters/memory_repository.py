from typing import List, Any
from games.domainmodel.model import Publisher, Genre, Game, User, Review, Wishlist
from .repository import AbstractRepository, RepositoryException


def get_game_title(game):
    return game.title


def get_game_description(game):
    return game.description


def get_game_publisher(game):
    return game.publisher.publisher_name


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__publishers = {}
        self.__genres = {}
        self.__games = {}
        self.__users = {}
        self.__reviews = []
        self.__wishlists = {}

    # Publisher Methods
    def add_publisher(self, publisher: Publisher) -> bool:
        if publisher.publisher_name not in self.__publishers:
            self.__publishers[publisher.publisher_name] = publisher
            return True
        raise RepositoryException(f'Publisher with name {publisher.publisher_name} already exists.')

    def add_multiple_publishers(self, publishers: List):
        for publisher in publishers:
            if publisher.publisher_name in self.__publishers:
                raise RepositoryException(f'Publisher with name {publisher.publisher_name} already exists.')
        for publisher in publishers:
            self.__publishers[publisher.publisher_name] = publisher

    def get_publisher(self, publisher_name: str) -> Publisher:
        return self.__publishers.get(publisher_name)

    # Genre Methods
    def add_genre(self, genre: Genre) -> bool:
        if genre.genre_name not in self.__genres:
            self.__genres[genre.genre_name] = genre
            return True
        raise RepositoryException(f'Genre with name {genre.genre_name} already exists.')

    def add_multiple_genres(self, genres: List):
        for genre in genres:
            if genre in self.__genres:
                raise RepositoryException(f'Genre with name {genre.genre_name} already exists.')
        for genre in genres:
            self.__genres[genre.genre_name] = genre

    def get_genre(self, genre_name: str) -> Genre:
        return self.__genres.get(genre_name)

    def get_genres(self) -> List[Genre]:
        return list(self.__genres.values())

    def get_games_by_genre(self, start_index, end_index, genre_name):
        games = [game for game in self.__games.values() if genre_name in [genre.genre_name for genre in game.genres]]
        return games[int(start_index):int(end_index)]

    def get_game_amount_by_genre(self, genre_name):
        # get the number of games of a specific genre
        all_games_of_genre = [game for game in self.__games.values() if
                              genre_name in [genre.genre_name for genre in game.genres]]
        return len(all_games_of_genre)

    # Game Methods
    def add_game(self, game: Game) -> bool:
        if game.game_id not in self.__games:
            self.__games[game.game_id] = game
            return True
        raise RepositoryException(f'Game with ID {game.game_id} already exists.')

    def add_multiple_games(self, games: List):
        for game in games:
            if game.game_id in self.__games:
                raise RepositoryException(f'Game with ID {game.game_id} already exists.')
        for game in games:
            self.__games[game.game_id] = game

    def get_game(self, game_id: int) -> Game:
        return self.__games.get(game_id)

    def search_games_by_key(self, term: str, key_str: str) -> List[Game]:
        key = get_game_title
        if key_str == "description":
            key = get_game_description
        elif key_str == "publisher":
            key = get_game_publisher
        return [game for game in self.__games.values() if isinstance(key(game), str) and
                term.lower() in key(game).lower()]

    def game_amount(self):
        return len(self.__games)

    def get_games_by_key(self, start_index, end_index, key_str):
        key = None
        reverse = False
        if key_str == "Newest":
            key = Game.date_sort_key
            reverse = True
        elif key_str == "Oldest":
            key = Game.date_sort_key
        # Sorting this list every time a request is made is probably a bad idea but like ¯\_(ツ)_/¯
        games = sorted(self.__games.values(), key=key, reverse=reverse)
        return games[start_index:end_index]

    # User Methods
    def add_user(self, user: User) -> bool:
        if user.username_unique not in self.__users:
            self.__users[user.username_unique] = user
            return True
        raise RepositoryException(f'User with username {user.username_unique} already exists.')

    def get_user(self, username: str) -> User:
        username = username.strip().lower()
        if username in self.__users:
            return self.__users[username]

    # Review Methods
    def add_review(self, review: Review) -> bool:
        if not isinstance(review, Review):
            raise RepositoryException('Invalid review object.')

        user = review.user
        game = review.game

        # Check if the review is already in the user's review list for the game in question
        if any(r for r in user.reviews if r.game == game):
            raise RepositoryException('User has already reviewed this game.')

        # Add the review to the user's reviews list
        user.add_review(review)
        game.reviews.append(review)

        # Add the game to the main repository's list of reviews so __reviews has all the games w reviews.
        if review not in self.__reviews:
            self.__reviews.append(review)

        return True

    def get_reviews_by_user(self, user_id) -> list:
        user_reviews = []
        for review in self.__reviews:
            if user_id == review.user.username_unique:
                user_reviews.append(review)
        return user_reviews

    def get_reviews_for_game(self, game_id) -> list:
        for review in self.__reviews:
            if review.game.game_id == game_id:
                print(review.game.reviews)
                return review.game.reviews
        return []

    # def reviews_per_user_limit(self, game_id, user_id) -> int:
    #     reviews = []
    #     for review in self.__reviews:
    #         if review.game.game_id == game_id and review.user.username_unique == user_id:
    #             reviews.append(review)
    #     return len(reviews)

    # Wishlist Methods
    def add_wishlist(self, wishlist: Wishlist) -> bool:
        if wishlist.user.username_unique not in self.__wishlists:
            self.__wishlists[wishlist.user.username_unique] = wishlist
            return True
        raise RepositoryException(f'Wishlist for user {wishlist.user.username_unique} already exists.')

    def get_wishlist(self, user: User) -> Any | None:
        if user is not None:
            return self.__wishlists.get(user.username_unique)
        else:
            return None

    def add_game_to_wishlist(self, user: User, game: Game) -> bool:
        """Add a game to a user's wishlist."""
        wishlist = self.get_wishlist(user)
        if not wishlist:
            # Create a new wishlist for the user if it doesn't exist
            wishlist = Wishlist(user)
            self.__wishlists[user.username_unique] = wishlist

        if game not in wishlist.list_of_games():
            wishlist.list_of_games().append(game)
            return True
        raise RepositoryException(
            f'Game with ID {game.game_id} is already in the wishlist of user {user.username_unique}.')

    def update_wishlist(self, user: User, new_wishlist: Wishlist) -> bool:
        """Update a user's wishlist."""
        if user.username_unique in self.__wishlists:
            self.__wishlists[user.username_unique] = new_wishlist
            return True
        raise RepositoryException(f'No wishlist found for user {user.username_unique}.')

    def remove_game_from_wishlist(self, user: User, game: Game) -> bool:
        wishlist = self.get_wishlist(user)
        if wishlist and game in wishlist.list_of_games():
            wishlist.list_of_games().remove(game)
            return True
        return False
