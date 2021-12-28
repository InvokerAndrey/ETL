import requests
import json

from .utils import backoff


class Load:
    BASE_URL = 'http://127.0.0.1:9200/'

    @backoff()
    def _load(self, url, query):
        return requests.post(
            url=url,
            headers={'Content-Type': 'application/x-ndjson'},
            data=query
        )

    def load_movies(self, movies):
        url = self.BASE_URL + '_bulk?filter_path=items.*.error'
        query = ""
        for movie in movies:
            query += json.dumps({"index": {"_index": "movies", "_id": movie["id"]}}) + '\n'
            query += json.dumps(movie) + '\n'
        return self._load(url, query)

    def load_movie(self, movie):
        url = self.BASE_URL + f"movies/_create/{movie['id']}"
        query = json.dumps({
            "doc": movie
        })
        return self._load(url, query)

    def update_movie(self, movie):
        url = self.BASE_URL + f"movies/_update/{movie['id']}"
        query = json.dumps({
            "doc": movie
        })
        return self._load(url, query)

    def delete_movie(self, movie_id):
        url = self.BASE_URL + 'movies/_delete_by_query'
        query = json.dumps({
            "query": {
                "match": {
                    "_id": movie_id
                }
            }
        })
        return self._load(url, query)

    def update_genre_in_movies(self, movies):
        url = self.BASE_URL + '_bulk?filter_path=items.*.error'
        query = ""
        for movie in movies:
            query += json.dumps({"update": {"_id": movie["id"], "_index": "movies"}}) + '\n'
            query += json.dumps({"doc": {"genre": movie['genre']}}) + '\n'
        return self._load(url, query)

    def update_person_in_movies(self, movies):
        url = self.BASE_URL + '_bulk?filter_path=items.*.error'
        query = ""
        for movie in movies:
            query += json.dumps({"update": {"_id": movie["id"], "_index": "movies"}}) + '\n'
            query += json.dumps({
                "doc": {
                    "actors": movie['actors'],
                    "writers": movie['writers'],
                    "director": movie['director'],
                    "actors_names": movie['actors_names'],
                    "writers_names": movie['writers_names'],
                }
            }) + '\n'
        return self._load(url, query)
