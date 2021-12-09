import math

from .extract import Extract
from .load import Load


class ExecuteETL:
    def __init__(self, db):
        self.db = db

    def exec(self):
        limit = 100
        offset = 0
        chunks_amount = math.ceil(Extract(self.db, limit, offset).get_movies_amount()[0]['count'] / limit)
        contents = []
        for _ in range(chunks_amount):
            response = Load(self.db).load_movies(limit=limit, offset=offset)
            offset += limit
            contents.append(response.content)
        return contents
