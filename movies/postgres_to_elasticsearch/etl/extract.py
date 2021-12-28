import logging

from .utils import backoff
from movies.models import Filmwork


class Extract:
    def get_movies(self, limit=100, offset=0):
        logging.info(f'Get {offset} : {offset + limit} rows')
        return Filmwork.objects.all()[offset:offset+limit]

    def get_movies_by_genre(self, genre, limit=100, offset=0):
        return Filmwork.objects.filter(genres=genre)[offset:offset+limit]

    def get_movies_by_ids(self, movies_ids, limit=100, offset=0):
        return Filmwork.objects.filter(id__in=movies_ids)[offset:offset+limit]

    def get_movies_by_person(self, person, limit=100, offset=0):
        return Filmwork.objects.filter(person=person)[offset:offset+limit]
