import math
from collections import defaultdict
from pathlib import Path
import os.path

from movies.models import PersonRole
from .etl.extract import Extract
from .etl.transform import Transform
from .etl.load import Load


class PipelineETL:
    def __init__(self):
        self.db = os.path.join(Path(__file__).resolve().parent.parent.parent, 'db.sqlite')
        self.extract = Extract(self.db)
        self.transform = Transform()
        self.load = Load()

    def _pipeline_genres(self):
        genres_str = self.extract.get_genres()
        transformed_genres = self.transform.validate_genres(genres_str)
        return self.load.save_genres(transformed_genres)

    def _pipeline_actors(self, limit, offset):
        batches_amount = math.ceil(self.extract.get_actors_amount()[0]['count'] / limit)
        actors = defaultdict(set)
        for _ in range(batches_amount):
            raw_actors = self.extract.get_actors(limit=limit, offset=offset)
            transformed_actors = self.transform.validate_actors(raw_actors)
            self.load.save_person(transformed_actors, PersonRole.ACTOR)
            for name, value in transformed_actors.items():
                actors[name] |= value
            offset += limit
        return actors

    def _pipeline_writers(self, limit, offset):
        batches_amount = math.ceil(self.extract.get_writers_amount()[0]['count'] / limit)
        writers = defaultdict(set)
        for _ in range(batches_amount):
            raw_writers = self.extract.get_writers(limit=limit, offset=offset)
            raw_movie_writers = self.extract.get_movie_writers()
            transformed_writers = self.transform.validate_writers(raw_writers, raw_movie_writers)
            self.load.save_person(transformed_writers, PersonRole.WRITER)
            for name, value in transformed_writers.items():
                writers[name] |= value
            offset += limit
        return writers

    def _pipeline_directors(self, limit, offset):
        batches_amount = math.ceil(self.extract.get_directors_amount()[0]['count'] / limit)
        directors = defaultdict(set)
        for _ in range(batches_amount):
            raw_directors = self.extract.get_directors(limit=limit, offset=offset)
            transformed_directors = self.transform.validate_directors(raw_directors)
            self.load.save_person(transformed_directors, PersonRole.DIRECTOR)
            for name, value in transformed_directors.items():
                directors[name] |= value
            offset += limit
        return directors

    def _pipeline_movies(self, limit, offset, actors, writers, directors):
        batches_amount = math.ceil(self.extract.get_movies_amount()[0]['count'] / limit)
        for _ in range(batches_amount):
            raw_movies = self.extract.get_movies(limit=limit, offset=offset)
            transformed_movies = self.transform.validate_movies(raw_movies, actors, writers, directors)
            self.load.save_movies(transformed_movies)
            offset += limit

    def run(self):
        limit = 100
        offset = 0

        self._pipeline_genres()
        actors = self._pipeline_actors(limit, offset)
        writers = self._pipeline_writers(limit, offset)
        directors = self._pipeline_directors(limit, offset)

        self._pipeline_movies(limit, offset, actors, writers, directors)
