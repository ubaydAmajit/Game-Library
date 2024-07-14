from sqlalchemy import select, inspect
from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['games', 'genres', 'publishers'], "Table names do not match!"


def test_database_populate_select_all_genres(database_engine):
    inspector = inspect(database_engine)
    name_of_genres_table = 'genres'

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert all_genre_names == ['Genre1', 'Genre2', 'Genre3'], "Genres do not match!"


def test_database_populate_select_all_games(database_engine):
    inspector = inspect(database_engine)
    name_of_games_table = 'games'

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['game_id'], row['title']))

        nr_games = len(all_games)
        assert nr_games == 100, "Number of games do not match!"
