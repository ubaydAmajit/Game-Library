"""Initialize Flask app."""

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import config
import games.adapters.datareader
import games.adapters.repository as repo
from games.adapters import repo_populate
from games.adapters.alchemy_repository import AlchemyRepository
from games.adapters.memory_repository import MemoryRepository
from games.utilities.copyright import copyright_rand

from games.adapters.orm import map_to_tables, metadata


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object(config.Config())
    data_path = "./games/adapters/data/games.csv"

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config["PRESET_DATA_PATH"]

    if app.config["REPOSITORY"] == "memory":
        repo.repo_instance = MemoryRepository()
        repo_populate.populate_data_from_file(repo.repo_instance, data_path)
    elif app.config["REPOSITORY"] == "alchemy":
        uri = app.config["ALCHEMY_URI"]
        engine = create_engine(uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=False)
        session_factory = sessionmaker(engine, autocommit=False, autoflush=True)
        repo.repo_instance = AlchemyRepository(session_factory)
        if app.config["TESTING"] == 'True' or len(engine.table_names()) == 0:
            print("Populating Empty Database")
            clear_mappers()
            metadata.create_all(engine)
            for table in reversed(metadata.sorted_tables):
                engine.execute(table.delete())
            map_to_tables()
            database_mode = True
            repo_populate.populate_data_from_file(repo.repo_instance, data_path)
            print("Completed Populating Database")


        else:
            map_to_tables()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .gamelibrary import gamelibrary
        app.register_blueprint(gamelibrary.library_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .auth import authentication
        app.register_blueprint(authentication.auth_blueprint)

        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

        from .reviews import reviews
        app.register_blueprint(reviews.reviews_blueprint)

    app.jinja_env.globals.update(copyright_rand=copyright_rand)

    return app
