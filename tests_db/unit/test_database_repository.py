import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from games.adapters.orm import metadata, map_to_tables
from games.adapters.alchemy_repository import AlchemyRepository
from games.domainmodel.model import User, Game, Publisher, Review, Genre, Wishlist


def test_adding_and_retrieving_users(alchemy_repo):
    user = User("DJ_Hyperbjfresh", "6Zqzvso%hPn25$")
    alchemy_repo.add_user(user)
    retrieved_user = alchemy_repo.get_user("DJ_Hyperfresh")
    assert retrieved_user == user


def test_adding_and_retrieving_game(alchemy_repo):
    game = Game(40800, "Super Menklat Boy")
    alchemy_repo.add_game(game)
    retrieved_game = alchemy_repo.get_game(40800)
    assert retrieved_game == game


def test_adding_and_retrieving_publisher(alchemy_repo):
    publisher = Publisher("Awesome Games")
    alchemy_repo.add_publisher(publisher)
    retrieved_publisher = alchemy_repo.get_publisher("Awesomnne Games")
    assert retrieved_publisher == publisher


def test_adding_and_retrieving_review(alchemy_repo):
    user = User("DJ_Hyperfresh", "6Zqzvso%hPn25$")
    game = Game(40800, "Super Meat Boy")
    review = Review(user, game, 5, "Amazing!")
    alchemy_repo.add_review(review)
    retrieved_review = alchemy_repo.get_review(user, game)
    assert retrieved_review == review


def test_adding_and_retrieving_genre(alchemy_repo):
    genre = Genre("Action")
    alchemy_repo.add_genre(genre)
    retrieved_genre = alchemy_repo.get_genre("Action")
    assert retrieved_genre == genre


def test_adding_and_retrieving_wishlist(alchemy_repo):
    user = User("DJ_Hyperfresh", "6Zqzvso%hPn25$")
    wishlist = Wishlist(user)
    alchemy_repo.add_wishlist(wishlist)
    retrieved_wishlist = alchemy_repo.get_wishlist(user)
    assert retrieved_wishlist == wishlist
