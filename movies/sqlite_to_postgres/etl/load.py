from django.db.utils import IntegrityError

import math

from .extract import Extract
from .transform import Transform
from movies.models import Filmwork, Genre, Person, FilmworkType, PersonRole


class Load:
    # def get_movie_person(self, lst, role, directors=False):
    #     result = []
    #     if lst:
    #         for person in lst:
    #             first_name = person if directors else person['name']
    #             if not Person.objects.filter(role=role, first_name=first_name).exists():
    #                 movie_person = Person.objects.create(
    #                     first_name=first_name,
    #                     role=role
    #                 )
    #             else:
    #                 movie_person = Person.objects.get(role=role, first_name=first_name)
    #             result.append(movie_person)
    #     return result
    #
    # def load_movies(self, limit, offset):
    #
    #     transform = Transform(self.db, limit, offset)
    #     movies = transform.get_movies_in_json()
    #     count = 0
    #     for movie in movies:
    #         # Genres
    #         movie_genres = []
    #         for genre in movie['genres'].split(', '):
    #             try:
    #                 movie_genre = Genre.objects.create(name=genre)
    #             except IntegrityError:
    #                 movie_genre = Genre.objects.get(name=genre)
    #             movie_genres.append(movie_genre)
    #
    #         # Person
    #         movie_actors = self.get_movie_person(movie['actors'], PersonRole.ACTOR)
    #         movie_directors = []
    #         if movie['directors']:
    #             movie_directors = self.get_movie_person(movie['directors'].split(', '), PersonRole.DIRECTOR, directors=True)
    #         movie_writers = self.get_movie_person(movie['writers'], PersonRole.WRITER)
    #
    #         # Movie
    #         film = Filmwork.objects.create(
    #             title=movie['title'],
    #             description=movie['description'],
    #             creation_date=None,
    #             certificate=None,
    #             rating=movie['rating'],
    #             type=FilmworkType.MOVIE,
    #         )
    #         for movie_genre in movie_genres:
    #             film.genres.add(movie_genre)
    #         for movie_actor in movie_actors:
    #             film.person.add(movie_actor)
    #         for movie_director in movie_directors:
    #             film.person.add(movie_director)
    #         for movie_writer in movie_writers:
    #             film.person.add(movie_writer)
    #         count += 1
    #         print(count, sep=' ')
    #
    # def save(self, limit=100, offset=0):
    #     chunks_amount = math.ceil(Extract(self.db, limit, offset).get_movies_amount()[0]['count'] / limit)
    #     for _ in range(chunks_amount):
    #         self.load_movies(limit=limit, offset=offset)
    #         offset += limit

    def save_genres(self, genres):
        return Genre.objects.bulk_create(
            [Genre(name=genre) for genre in genres]
        )
