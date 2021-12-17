import math
from collections import defaultdict

from .extract import Extract
from .transform import Transform
from .load import Load


def run():
    db = 'db.sqlite'
    limit = 100
    offset = 0

    extract = Extract(db)
    transform = Transform()
    load = Load()

    batches_amount = math.ceil(extract.get_movies_amount()[0]['count'] / limit)

    genres = defaultdict(set)
    for i in range(batches_amount):
        raw_genres = extract.get_genres(limit=limit, offset=offset)
        transformed_genres = transform.validate_genres(raw_genres)
        for key in transformed_genres.keys():
            genres[key] |= transformed_genres[key]
        offset += limit

    # load.save_genres(genres)

    # genres = transform.validate_genres(genres)
    #genres_qs = load.save_genres(genres)

# data = extract_genres_from_sqlite()
# transformed_data = transform(data)
# loader.save(transformed_data)
#
# # person
# #  > 100k
# # butch_size=1000 with offset
# persons_cache = {}
# # add cycly for + limit offset
#
# for persons_data in extract_persons(limit, offset):
#     # persons_cache
#     #
#
#
#
#
# films_data = extract_films_from_sqlite()
#
# genres_data = extrator_genres_from_psql
# persons_data = extrator_persons_from_psql
#
# transformed_data = transform(films_data, genres_data, persons_data)
# loader.save(transformed_data)
