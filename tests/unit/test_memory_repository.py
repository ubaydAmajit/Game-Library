import pytest

from games.adapters.repository import RepositoryException
from games.domainmodel.model import Game, User, Review, Wishlist


def test_repo_get_game(in_memory_repo):
    game = in_memory_repo.get_game(40800)
    assert game == Game(40800, "Super Meat Boy")


def test_repo_get_nonexistent_game(in_memory_repo):
    game = in_memory_repo.get_game(1)
    assert game is None


def test_repo_search_games(in_memory_repo):
    description_game = in_memory_repo.search_games_by_key("MURI is a DOS-style", "description")
    assert description_game == [Game(267360, "MURI")]
    title_game = in_memory_repo.search_games_by_key("super meat boy", "title")
    assert title_game == [Game(40800, "Super Meat Boy")]
    publisher_game = in_memory_repo.search_games_by_key("encore", "publisher")
    assert publisher_game == [Game(243890, "Mavis Beacon Teaches Typing Family Edition")]


def test_repo_get_ordered_games(in_memory_repo):
    oldest_games = in_memory_repo.get_games_by_key(0, 3, "Oldest")
    assert (str(oldest_games) ==
            "[<Game 3010, Xpand Rally>, <Game 7940, Call of Duty® 4: Modern Warfare®>, <Game 16130, Fish Tycoon>]")
    newest_games = in_memory_repo.get_games_by_key(0, 3, "Newest")
    assert (str(newest_games) ==
            "[<Game 2010700, Hunter Survivors>, <Game 1995240, Deer Journey>, <Game 2061060, The Marson Home>]")


def test_repo_can_retrieve_genres(in_memory_repo):
    genres = in_memory_repo.get_genres()
    simulation = None
    for genre in genres:
        if genre.genre_name == "Simulation":
            simulation = genre
    assert simulation.number_of_games == 167


def test_repo_get_genre(in_memory_repo):
    genre = in_memory_repo.get_genre("Racing")
    assert genre.number_of_games == 31


def test_repo_get_genre_not_exist(in_memory_repo):
    # Check None is returned when Non-Existent Genre is Requested
    genre = in_memory_repo.get_genre("NFSW")
    assert genre is None


def test_add_get_user(in_memory_repo):
    in_memory_repo.add_user(User("DJ_Hyperfresh", "6Zqzvso%hPn25$"))
    user = in_memory_repo.get_user("DJ_Hyperfresh")
    assert user == User("DJ_Hyperfresh", "6Zqzvso%hPn25$")


def test_no_duplicate_users(in_memory_repo):
    # Pearlina Wedding DLC
    in_memory_repo.add_user(User("DJ_Hyperfresh", "6Zqzvso%hPn25$"))
    in_memory_repo.add_user(User("MC.Princess", "6Zqzvso%hPn25$"))
    with pytest.raises(RepositoryException):
        in_memory_repo.add_user(User("DJ_Hyperfresh", "6Zqzvso%hPn25$"))


def test_get_publisher(in_memory_repo):
    publisher = in_memory_repo.get_publisher("Pablo Picazo")
    assert str(publisher) == "<Publisher Pablo Picazo>"


def test_get_add_get_reviews(in_memory_repo):
    in_memory_repo.add_review(Review(
        User("DJ_Hyperfresh", "6Zqzvso%hPn25$"),
        Game(1, "Splatoon 3"),
        5,
        "Gay <3"
    ))

    review = in_memory_repo.get_reviews_for_game(1)[0]
    assert str(review) == "Review(User: <User dj_hyperfresh>, Game: <Game 1, Splatoon 3>, Rating: 5, Comment: Gay <3)"


def test_get_add_wishlist(in_memory_repo):
    in_memory_repo.add_wishlist(Wishlist(User("DJ_Hyperfresh", "6Zqzvso%hPn25$")))
    assert (in_memory_repo.get_wishlist(User("DJ_Hyperfresh", "6Zqzvso%hPn25$")).user ==
            User("DJ_Hyperfresh", "6Zqzvso%hPn25$"))


def test_add_duplicates_wishlist(in_memory_repo):
    in_memory_repo.add_wishlist(Wishlist(User("DJ_Hyperfresh", "6Zqzvso%hPn25$")))
    with pytest.raises(RepositoryException):
        in_memory_repo.add_wishlist(Wishlist(User("DJ_Hyperfresh", "6Zqzvso%hPn25$")))


def test_get_games_by_genre(in_memory_repo):
    games = in_memory_repo.get_games_by_genre(0, 3, "Racing")
    assert len(games) == 3


def test_get_games_pagination(in_memory_repo):
    games_page_1 = in_memory_repo.get_games_by_key(1, 3, "Newest")
    games_page_2 = in_memory_repo.get_games_by_key(2, 3, "Newest")
    assert games_page_1[0].date_sort_key() >= games_page_2[0].date_sort_key()
