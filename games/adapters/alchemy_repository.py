from sqlite3 import IntegrityError
from typing import List

from sqlalchemy import exists, desc, func
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import scoped_session

from games.adapters.repository import AbstractRepository, RepositoryException, KeyException
from games.domainmodel.model import Publisher, User, Review, Genre, Game, Wishlist


class SessionContextManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = scoped_session(self.session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.session = scoped_session(self.session_factory)

    def close_current_session(self):
        if self.session is not None:
            self.session.close()


class AlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self.session_context_manager = SessionContextManager(session_factory)

    def close_session(self):
        self.session_context_manager.close_current_session()

    def reset_session(self):
        self.session_context_manager.reset_session()

    def add_publisher(self, publisher: Publisher):
        with self.session_context_manager as scm:
            scm.session.add(publisher)
            scm.commit()

    def add_multiple_publishers(self, publishers: List):
        with self.session_context_manager as scm:
            for publisher in publishers:
                scm.session.add(publisher)
            scm.commit()

    def get_publisher(self, publisher_name: str) -> Publisher:
        publisher = None
        try:
            publisher = self.session_context_manager.session.query(Publisher).filter(
                Publisher.publisher_name == publisher_name).one()
        except NoResultFound:
            pass
        return publisher

    def add_genre(self, genre: Genre):
        with self.session_context_manager as scm:
            try:
                scm.session.add(genre)
                scm.commit()
            except IntegrityError:
                raise RepositoryException(f'Genre with name {genre.genre_name} already exists.')

    def add_multiple_genres(self, genres: List):
        with self.session_context_manager as scm:
            for genre in genres:
                scm.session.add(genre)
            scm.commit()

    def get_genre(self, genre_name: str) -> Genre:
        genre = None
        try:
            genre = self.session_context_manager.session.query(Genre).filter(
                Genre.genre_name == genre_name
            ).one()
        except NoResultFound:
            pass
        return genre

    def get_genres(self) -> List[Genre]:
        genres = None
        try:
            genres = self.session_context_manager.session.query(Genre).all()
        except NoResultFound:
            pass
        return genres

    def get_games_by_genre(self, start_index, end_index, genre_name):
        games = None
        try:
            games = (
                self.session_context_manager
                .session.query(Game)
                .join(Genre)
                .filter(Genre.genre_name)
                .limit(end_index - start_index)
                .offset(start_index)
                .all()
            )
        except NoResultFound:
            pass
        return games

    def add_game(self, game: Game):
        with self.session_context_manager as scm:
            scm.session.add(game)
            scm.commit()

    def add_multiple_games(self, games: List):
        with self.session_context_manager as scm:
            for game in games:
                scm.session.add(game)
            scm.commit()

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self.session_context_manager.session.query(Game).filter(
                Game._Game__game_id == game_id
            ).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')
        return game

    def search_games_by_key(self, term: str, key) -> List[Game]:
        match key:
            case 'title':
                query_filter = Game._Game__game_title
            case 'description':
                query_filter = Game._Game__description
            case 'publisher':
                query_filter = Game._Game__publisher
            case _:
                raise KeyException(f"Invalid Key: {key}")

        games = self.session_context_manager.session.query(Game).filter(query_filter.like(f"%{term}%")).all()

        return games

    def game_amount(self):
        return self.session_context_manager.session.query(Game).count()

    def get_games_by_key(self, start_index, end_index, key):
        match key:
            case "Newest":
                sort_key = desc(Game._Game__release_date)
            case "Oldest":
                sort_key = Game._Game__release_date
            case _:
                raise KeyException("Invalid Key")
        return (self.session_context_manager.session
                .query(Game)
                .order_by(sort_key)
                .offset(start_index)
                .limit(end_index - start_index)
                .all())

    def add_user(self, user: User):
        with self.session_context_manager as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            user = self.session_context_manager.session.query(User).filter(
                func.lower(User._User__username) == func.lower(username)
            ).one()
        except NoResultFound:
            pass
        return user

    def add_review(self, review: Review):
        with self.session_context_manager as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews_by_user(self, user_id) -> list:
        return (self.session_context_manager.session
                .query(Review)
                .join(User)
                .filter(func.lower(user_id) == func.lower(User._User__username))
                .all())

    def get_reviews_for_game(self, game_id):
        return (self.session_context_manager.session
                .query(Review)
                .join(Game)
                .filter(game_id == Game._Game__game_id)
                .all())

    # def reviews_per_user_limit(self, game_id, user_id) -> int:
    #     return (self.session_context_manager.session
    #             .query(Review)
    #             .filter(Review._Review__game == game_id)
    #             .filter(Review._Review__user == user_id)
    #             .count())

    def add_wishlist(self, wishlist: Wishlist):
        with self.session_context_manager as scm:
            scm.session.add(wishlist)
            scm.commit()

    def get_wishlist(self, user: User) -> Wishlist:
        wishlist = None
        try:
            wishlist = (self.session_context_manager.session
                        .query(Wishlist)
                        .join(User)
                        .filter(func.lower(User._User__username) == func.lower(user._User__username))
                        .one())
        except NoResultFound:
            pass
        return wishlist

    def add_game_to_wishlist(self, user: User, game: Game) -> bool:
        with self.session_context_manager as scm:
            wishlist = self.get_wishlist(user)
            if wishlist is None:
                wishlist = Wishlist(user)
                scm.session.add(wishlist)
            wishlist.add_game(game)
            self.session_context_manager.commit()
            return True

    def update_wishlist(self, user: User, new_wishlist: Wishlist) -> bool:
        with self.session_context_manager as scm:
            scm.session.merge(new_wishlist)
            return True

    def remove_game_from_wishlist(self, user: User, game: Game):
        with self.session_context_manager as scm:
            self.get_wishlist(user).remove_game(game)
            self.session_context_manager.commit()
            return True
