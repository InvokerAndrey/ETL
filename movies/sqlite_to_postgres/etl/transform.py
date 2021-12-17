import json
from typing import List
from collections import defaultdict

from .extract import Extract


class Transform:
    # def get_valid_movies(self):
    #     """ Replace 'N/A' to None in description and director fields """
    #     movies = self.extract.get_movies()
    #     for movie in movies:
    #         if movie['director'] == 'N/A':
    #             movie['director'] = None
    #         if movie['plot'] == 'N/A':
    #             movie['plot'] = None
    #         if movie['imdb_rating'] == 'N/A':
    #             movie['imdb_rating'] = None
    #     return movies

    # def get_single_movie_actors(self, movie):
    #     actors = self.extract.get_single_movie_actors(movie['id'])
    #     count = 0
    #     for actor in actors:
    #         if actor['name'] == 'N/A':
    #             actor['name'] = None
    #             count += 1
    #     return actors

    # def get_single_movie_actors_names(self, actors):
    #     return ', '.join(str(actor['name']) for actor in actors)
    #
    # def get_single_movie_writers(self, movie):
    #     if movie['writers']:
    #         writers = json.loads(movie['writers'])
    #         writers_ids = [writer['id'] for writer in writers]
    #         return self.extract.get_writers_by_ids(writers_ids)
    #     return None
    #
    # def get_single_movie_writers_names(self, writers):
    #     if writers:
    #         return ', '.join(writer['name'] for writer in writers)
    #     return None

    # def get_movies_in_json(self):
    #     json_movies = []
    #     all_movies = self.get_valid_movies()
    #     for movie in all_movies:
    #         actors = self.get_single_movie_actors(movie)
    #         writers = self.get_single_movie_writers(movie)
    #         json_movie = {
    #             'actors': actors,
    #             'description': movie['plot'],
    #             'directors': movie['director'],
    #             'genres': movie['genre'],
    #             'id': movie['id'],
    #             'rating': movie['imdb_rating'],
    #             'title': movie['title'],
    #             'writers': writers,
    #         }
    #         json_movies.append(json_movie)
    #     return json_movies

    def validate_genres(self, raw_genres: List[dict]):
        genres = defaultdict(set)
        for raw_genre in raw_genres:
            for genre in raw_genre['genre'].split(', '):
                genres[genre].add(raw_genre['id'])
        return genres
