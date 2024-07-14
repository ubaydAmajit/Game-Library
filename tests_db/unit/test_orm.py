from games.domainmodel.model import User, Game, Publisher, Review, Genre, Wishlist
from games.adapters.orm import map_to_tables


def test_adding_and_retrieving_user(session_factory):
    map_to_tables()
    user = User("DJ_Hyperfresh", "password")
    session = session_factory()
    session.add(user)
    session.commit()
    session2 = session_factory()
    retrieved_user = session2.query(User).first()
    assert retrieved_user.username == "DJ_Hyperfresh"


def test_adding_and_retrieving_game(session_factory):
    map_to_tables()
    game = Game(1, "Super Meat Boy")
    publisher = Publisher("Team Meat")
    game.publisher = publisher
    session = session_factory()
    session.add(game)
    session.commit()
    session2 = session_factory()
    retrieved_game = session2.query(Game).first()
    assert retrieved_game.title == "Super Meat Boy"
    assert retrieved_game.publisher.publisher_name == "Team Meat"


def test_adding_and_retrieving_publisher(session_factory):
    # Given
    map_to_tables()
    publisher = Publisher("Nintendo")

    # When
    session = session_factory()
    session.add(publisher)
    session.commit()

    # Then
    session2 = session_factory()
    retrieved_publisher = session2.query(Publisher).first()
    assert retrieved_publisher.publisher_name == "Nintendo"


def test_adding_and_retrieving_review(session_factory):
    map_to_tables()
    user = User("DJ_Hyperfresh", "password")
    game = Game(1, "Super Meat Boy")
    review = Review(user, game, 5, "Loved it!")
    session = session_factory()
    session.add(review)
    session.commit()
    session2 = session_factory()
    retrieved_review = session2.query(Review).first()
    assert retrieved_review.comment == "Loved it!"
    assert retrieved_review.user.username == "DJ_Hyperfresh"
    assert retrieved_review.game.title == "Super Meat Boy"


def test_adding_and_retrieving_genre(session_factory):
    map_to_tables()
    genre = Genre("Platformer")
    session = session_factory()
    session.add(genre)
    session.commit()
    session2 = session_factory()
    retrieved_genre = session2.query(Genre).first()
    assert retrieved_genre.genre_name == "Platformer"


def test_adding_and_retrieving_wishlist(session_factory):
    map_to_tables()
    user = User("MC.Princess", "securepassword")
    game1 = Game(2, "Zelda")
    game2 = Game(3, "Mario")
    wishlist = Wishlist(user)
    wishlist.add_game(game1)
    wishlist.add_game(game2)

    # When
    session = session_factory()
    session.add(wishlist)
    session.commit()

    # Then
    session2 = session_factory()
    retrieved_wishlist = session2.query(Wishlist).first()
    assert retrieved_wishlist.user.username == "MC.Princess"
    assert len(retrieved_wishlist.list_of_games) == 2

