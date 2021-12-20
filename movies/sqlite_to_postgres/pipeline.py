import math
from collections import defaultdict
from pathlib import Path
import os.path

from .etl.extract import Extract
from .etl.transform import Transform
from .etl.load import Load


def etl_genres(extract, transform, load):
    genres_str = extract.get_genres()
    transformed_genres = transform.validate_genres(genres_str)
    return load.save_genres(transformed_genres)


def etl_actors(limit, offset, extract, transform, load):
    batches_amount = math.ceil(extract.get_actors_amount()[0]['count'] / limit)
    actors = defaultdict(set)
    for _ in range(batches_amount):
        raw_actors = extract.get_actors(limit=limit, offset=offset)
        transformed_actors = transform.validate_actors(raw_actors)
        load.save_actors(transformed_actors)
        for name, value in transformed_actors.items():
            actors[name] |= value
        offset += limit
    return actors


def etl_writers(limit, offset, extract, transform, load):
    batches_amount = math.ceil(extract.get_writers_amount()[0]['count'] / limit)
    writers = defaultdict(set)
    for _ in range(batches_amount):
        raw_writers = extract.get_writers(limit=limit, offset=offset)
        raw_movie_writers = extract.get_movie_writers()
        transformed_writers = transform.validate_writers(raw_writers, raw_movie_writers)
        load.save_writers(transformed_writers)
        for name, value in transformed_writers.items():
            writers[name] |= value
        offset += limit
    return writers


def etl_directors(limit, offset, extract, transform, load):
    batches_amount = math.ceil(extract.get_directors_amount()[0]['count'] / limit)
    directors = defaultdict(set)
    for _ in range(batches_amount):
        raw_directors = extract.get_directors(limit=limit, offset=offset)
        transformed_directors = transform.validate_directors(raw_directors)
        load.save_directors(transformed_directors)
        for name in transformed_directors:
            directors[name] |= transformed_directors[name]
        offset += limit
    return directors


def etl_movies(limit, offset, extract, transform, load):
    genres = etl_genres(extract, transform, load)
    actors = etl_actors(limit, offset, extract, transform, load)
    writers = etl_writers(limit, offset, extract, transform, load)
    directors = etl_directors(limit, offset, extract, transform, load)

    batches_amount = math.ceil(extract.get_movies_amount()[0]['count'] / limit)
    movies = []


def run():
    db = os.path.join(Path(__file__).resolve().parent.parent.parent, 'db.sqlite')
    limit = 100
    offset = 0

    extract = Extract(db)
    transform = Transform()
    load = Load()

    etl_movies(limit, offset, extract, transform, load)


if __name__ == '__main__':
    run()
