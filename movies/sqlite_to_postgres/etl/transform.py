import json
from typing import List
from collections import defaultdict

from movies.models import Genre, Person, PersonRole


class Transform:
    def validate_genres(self, genres_str: str) -> set:
        """
        :param genres_str: 'Action, Adventure, Action, Sci-Fi, ...'
        :return: {'Action', 'Adventure', 'Sci-Fi', ...}
        """
        return set(genres_str.split(', '))

    def validate_actors(self, raw_actors: List[dict]):
        """
        :param raw_actors: [
            {
                'name': actor_name,
                'movie_id': movie_id
            },
            ...
        ]
        :return: {
            actor_name: { movie_id, movie_id, ... }
        }
        """
        actors = defaultdict(set)
        for raw_actors in raw_actors:
            actors[raw_actors['name']].add(raw_actors['movie_id'])
        return actors

    def validate_writers(self, raw_writers: List[dict], movies: List[dict]):
        """
        :param raw_writers: [
            {
                'id': writer.id,
                'name': writer.name
            },
            ...
        ]
        :param movies: [
            {
                'movie_id': movie.id,
                'writers': "[{'id': writer.id}, ...]",
                'writer': 'writer_id'
            },
            ...
        ]
        :return: { writer_name: {movie_id, ...} }
        """
        writers = defaultdict(set)
        for raw_writer in raw_writers:
            name = raw_writer['name']
            writers[name] |= set()
            for movie in movies:
                if raw_writer['id'] == movie['writer']:
                    writers[name].add(movie['movie_id'])
                    continue
                if not movie['writers']:
                    continue
                for raw_writer_id in json.loads(movie['writers']):
                    if raw_writer['id'] == raw_writer_id['id']:
                        writers[name].add(movie['movie_id'])
        return writers

    def validate_directors(self, raw_directors):
        """
        :param raw_directors: [
            {
                'movie_id': movie_id,
                'director': ['director.name',...],
            },
            ...
        ]
        :return: {
            director_name: { movie_id, movie_id, ... }
        }
        """
        directors = defaultdict(set)
        for raw_director in raw_directors:
            for name in raw_director['director'].split(', '):
                directors[name].add(raw_director['movie_id'])
        return directors

    def validate_movies(self, raw_movies, actors, writers, directors):
        """
        :param raw_movies: [
            {
                'old_id': id,
                'title': title,
                'genre': genre,
                'description': description,
                'rating': imdb_rating
            },
            ...
        ]
        :return: [
            {
                'old_id': id,
                'title': title,
                'description': description,
                'rating': imdb_rating,
                'genres': genres_qs,
                'actors': [ actor_qs, ... ],
                'writers': [ writer_qs, ... ],
                'directors': [ director_qs, ... ]
            },
            ...
        ]
        """
        for raw_movie in raw_movies:
            if raw_movie['description'] == 'N/A':
                raw_movie['description'] = None
            if raw_movie['rating'] == 'N/A':
                raw_movie['rating'] = None

            # Genres
            genres = Genre.objects.filter(name__in=raw_movie['genre'].split(', '))
            del raw_movie['genre']
            raw_movie['genres'] = genres

            # Person
            self.transform_person_for_movie(actors, raw_movie, 'actors', PersonRole.ACTOR)
            self.transform_person_for_movie(writers, raw_movie, 'writers', PersonRole.WRITER)
            self.transform_person_for_movie(directors, raw_movie, 'directors', PersonRole.DIRECTOR)
        return raw_movies

    def transform_person_for_movie(self, person, raw_movie, person_type, role):
        person_names = []
        for name, movie_ids in person.items():
            if raw_movie['old_id'] in movie_ids:
                person_names.append(name)
        querysets = Person.objects.none()
        for name in person_names:
            split_name = name.split(maxsplit=1)
            first_name = split_name[0]
            last_name = split_name[1] if len(split_name) > 1 else ''
            querysets |= Person.objects.filter(role=role, first_name=first_name, last_name=last_name)
        raw_movie[person_type] = querysets
