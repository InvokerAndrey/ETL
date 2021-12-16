import sqlite3


class Extract:
    def __init__(self, db, limit, offset):
        self.db = db
        self.limit = limit
        self.offset = offset

    def execute_sql(self, sql, args_lst=None):
        with sqlite3.connect(self.db) as connection:
            # for dict conversion
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            if args_lst:
                cursor.execute(sql, args_lst)
            else:
                cursor.execute(sql)
            return [dict(x) for x in cursor.fetchall()]

    def get_movies_amount(self):
        sql = "SELECT COUNT(*) as 'count' FROM movies"
        return self.execute_sql(sql)

    def get_movies(self):
        sql = f"SELECT * FROM movies ORDER BY id LIMIT {self.limit} OFFSET {self.offset}"
        return self.execute_sql(sql)

    def get_writers(self):
        sql = "SELECT * FROM writers WHERE name != 'N/A'"
        return self.execute_sql(sql)

    def get_writers_by_ids(self, writers_ids):
        sql = "SELECT * FROM writers WHERE id IN (%s)" % ','.join('?' for _ in writers_ids)
        return self.execute_sql(sql, writers_ids)

    def get_single_movie_actors(self, movie_id):
        sql = "SELECT actors.id, actors.name FROM actors " \
              "JOIN movie_actors ON actor_id = actors.id " \
              "JOIN movies ON movie_id = movies.id " \
              "WHERE movies.id = ?"
        return self.execute_sql(sql, [movie_id])
