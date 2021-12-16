from django.db.utils import IntegrityError

import json
import requests

from .transform import Transform
from movies.models import Filmwork, Genre, Person, FilmworkType, PersonRole


class Load:
    def __init__(self, db):
        self.db = db

    def create_movies(self):
        transform = Transform(self.db)
        movies = transform.get_movies_in_json()
        for movie in movies:
            # Genres
            movie_genres = []
            for genre in movie['genres'].split(', '):
                try:
                    movie_genre = Genre.objects.create(name=genre)
                except IntegrityError:
                    movie_genre = Genre.objects.get(name=genre)
                movie_genres.append(movie_genre)

            # Actors
            movie_actors = []
            if movie['actors']:
                for actor in movie['actors']:
                    first_name = actor['name']
                    if not Person.objects.filter(role=PersonRole.ACTOR, first_name=first_name).exists():
                        movie_actor = Person.objects.create(
                            first_name=first_name,
                            role=PersonRole.ACTOR
                        )
                    else:
                        movie_actor = Person.objects.get(role=PersonRole.ACTOR, first_name=first_name)
                    movie_actors.append(movie_actor)

            # Directors
            movie_directors = []
            if movie['directors']:
                for director in movie['directors'].split(', '):
                    first_name = director
                    if not Person.objects.filter(role=PersonRole.DIRECTOR, first_name=first_name):
                        movie_director = Person.objects.create(
                            first_name=first_name,
                            role=PersonRole.DIRECTOR
                        )
                    else:
                        movie_director = Person.objects.get(role=PersonRole.DIRECTOR, first_name=first_name)
                    movie_directors.append(movie_director)

            # Writers
            movie_writers = []
            if movie['writers']:
                for writer in movie['writers']:
                    first_name = writer['name']
                    if not Person.objects.filter(role=PersonRole.WRITER, first_name=first_name):
                        movie_writer = Person.objects.create(
                            first_name=first_name,
                            role=PersonRole.WRITER
                        )
                    else:
                        movie_writer = Person.objects.get(role=PersonRole.WRITER, first_name=first_name)
                    movie_writers.append(movie_writer)

            # Movie
            film = Filmwork.objects.create(
                title=movie['title'],
                description=movie['description'],
                creation_date=None,
                certificate=None,
                rating=movie['rating'],
                type=FilmworkType.MOVIE,
            )
            for movie_genre in movie_genres:
                film.genres.add(movie_genre)
            for movie_actor in movie_actors:
                film.person.add(movie_actor)
            for movie_director in movie_directors:
                film.person.add(movie_director)
            for movie_writer in movie_writers:
                film.person.add(movie_writer)

    def load_movies(self, limit, offset):
        transform = Transform(self.db, limit, offset)
        movies = transform.get_movies_in_json()
        query = ""
        for movie in movies:
            query += json.dumps({"index": {"_index": "movies", "_id": movie["id"]}}) + '\n'
            query += json.dumps(movie) + '\n'

        return requests.post(
            "http://127.0.0.1:9200/_bulk?filter_path=items.*.error",
            headers={'Content-Type': 'application/x-ndjson'},
            data=query
        )
