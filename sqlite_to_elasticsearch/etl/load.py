import json
import requests

from .transform import Transform


class Load:
    def __init__(self, db):
        self.db = db

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
