import sqlite3


class Extract:
    def __init__(self, db):
        self.db = db

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

    def get_actors_amount(self):
        sql = "SELECT COUNT(*) as 'count' FROM actors WHERE name != 'N/A'"
        return self.execute_sql(sql)

    def get_writers_amount(self):
        sql = "SELECT COUNT(*) as 'count' FROM writers WHERE name != 'N/A'"
        return self.execute_sql(sql)

    def get_directors_amount(self):
        sql = "SELECT COUNT(*) as 'count' FROM movies WHERE director != 'N/A'"
        return self.execute_sql(sql)

    def get_genres(self):
        sql = "SELECT group_concat(genre, ', ') as genres FROM (SELECT DISTINCT genre FROM movies)"
        return self.execute_sql(sql)[0]['genres']

    def get_actors(self, limit=100, offset=0):
        sql = f"SELECT actors.name, movie_actors.movie_id FROM actors " \
              f"JOIN movie_actors ON movie_actors.actor_id = actors.id " \
              f"WHERE actors.name != 'N/A' LIMIT {limit} OFFSET {offset} "
        return self.execute_sql(sql)

    def get_movies(self, limit, offset):
        sql = f"SELECT id as 'old_id', title, genre, plot as 'description', imdb_rating as 'rating' from movies " \
              f"ORDER BY id LIMIT {limit} OFFSET {offset}"
        return self.execute_sql(sql)

    def get_writers(self, limit=100, offset=0):
        sql = f"SELECT * FROM writers WHERE name != 'N/A' LIMIT {limit} OFFSET {offset}"
        return self.execute_sql(sql)

    def get_movie_writers(self, limit=100, offset=0):
        sql = f"SELECT id as 'movie_id', writers, writer FROM movies ORDER BY id LIMIT {limit} OFFSET {offset}"
        return self.execute_sql(sql)

    def get_directors(self, limit=100, offset=0):
        sql = f"SELECT id as 'movie_id', director FROM movies WHERE director != 'N/A' LIMIT {limit} OFFSET {offset}"
        return self.execute_sql(sql)
