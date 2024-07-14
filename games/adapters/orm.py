from sqlalchemy import (Table, MetaData, Column, Integer, String, ForeignKey, Date, Boolean)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel import model

metadata = MetaData()

user_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255, collation='NOCASE'), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column("date_joined", Date, nullable=False)
)

favourite_games_table = Table(
    'favourites', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('game_id', ForeignKey('games.id'))
)

wishlist_game_table = Table(
    'wishlist_games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('wishlist_id', ForeignKey('wishlists.id')),
    Column('game_id', ForeignKey('games.id'))
)

wishlist_table = Table(
    'wishlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'))
)

publisher_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)
)

game_table = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('price', Integer),
    Column('release_date', Date),
    Column('description', String(2048)),
    Column('image_url', String(255)),
    Column('website_url', String(255)),
    Column('linux', Boolean),
    Column('windows', Boolean),
    Column('mac', Boolean),
    Column('publisher_name', ForeignKey('publishers.name'))
)

genre_table = Table(
    'genres', metadata,
    Column('name', String(255), primary_key=True, unique=True, nullable=False)
)

game_genre_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.id')),
    Column('genre', ForeignKey('genres.name'))
)

review_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.id'), nullable=False),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('comment', String(500), nullable=False)
)


def map_to_tables():
    mapper(model.User, user_table, properties={
        '_User__username': user_table.c.username,
        '_User__password': user_table.c.password,
        '_User__date_joined': user_table.c.date_joined,
        '_User__favourite_games': relationship(model.Game, secondary=favourite_games_table)
    })

    mapper(model.Review, review_table, properties={
        '_Review__user': relationship(model.User, backref='_User__reviews'),
        '_Review__game': relationship(model.Game, backref='_Game__reviews'),
        '_Review__rating': review_table.c.rating,
        '_Review__comment': review_table.c.comment
    })

    mapper(model.Game, game_table, properties={
        '_Game__game_title': game_table.c.title,
        '_Game__game_id': game_table.c.id,
        '_Game__price': game_table.c.price,
        '_Game__release_date': game_table.c.release_date,
        '_Game__description': game_table.c.description,
        '_Game__image_url': game_table.c.image_url,
        '_Game__website_url': game_table.c.website_url,
        '_Game__supports_linux': game_table.c.linux,
        '_Game__supports_windows': game_table.c.windows,
        '_Game__supports_mac': game_table.c.mac,
        '_Game__genres': relationship(model.Genre, secondary=game_genre_table, backref="_Genre__games"),
        '_Game__publisher': relationship(model.Publisher)
    })

    mapper(model.Genre, genre_table, properties={
        '_Genre__genre_name': genre_table.c.name,
    })

    mapper(model.Publisher, publisher_table, properties={
        '_Publisher__publisher_name': publisher_table.c.name
    })

    mapper(model.Wishlist, wishlist_table, properties={
        '_Wishlist__user': relationship(model.User),
        '_Wishlist__list_of_games': relationship(model.Game, secondary=wishlist_game_table)
    })
