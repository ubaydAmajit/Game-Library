from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre


def populate_data_from_file(repo: AbstractRepository, file_path):
    reader = GameFileCSVReader(file_path)
    reader.read_csv_file()

    repo.add_multiple_games(reader.dataset_of_games)
    repo.add_multiple_genres(reader.dataset_of_genres.values())
    repo.add_multiple_publishers(reader.dataset_of_publishers.values())
