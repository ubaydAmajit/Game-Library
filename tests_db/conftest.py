import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games.adapters import alchemy_repository, repo_populate
from games.adapters.orm import metadata, map_to_tables

from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent


TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "games" / "adapters" / "data" / "games.csv"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///:memory:'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = alchemy_repository.AlchemyRepository(session_factory)
    database_mode = True
    repo_populate.populate_data_from_file(repo_instance, TEST_DATA_PATH_DATABASE_FULL)
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = alchemy_repository.AlchemyRepository(session_factory)
    database_mode = True
    repo_populate.populate_data_from_file(repo_instance, TEST_DATA_PATH_DATABASE_FULL)
    yield session_factory
    metadata.drop_all(engine)


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_to_tables()
    session_factory = sessionmaker(bind=engine)
    with session_factory() as session:
        yield session
    metadata.drop_all(engine)
