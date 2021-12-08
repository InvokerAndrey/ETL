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

    def get_actors(self):
        """ Get actors without 'N/A' values """
        sql = "SELECT * FROM actors WHERE name != 'N/A'"
        return self.execute_sql(sql)

    def get_actors_ids(self, actors):
        """ Get IDs of actors that are without 'N/A' values """
        return [actor['id'] for actor in actors]

    def get_movie_actors(self):
        """ Get movie_actors rows which don't contain actors with 'N/A' values """
        actors_ids = self.get_actors_ids(self.get_actors())
        sql = "SELECT * FROM movie_actors WHERE actor_id IN (%s)" % ','.join('?' for _ in actors_ids)
        # Passing actors_ids to avoid sql injections (execute method will match list of '?' with actors_ids)
        return self.execute_sql(sql, actors_ids)

    def get_movie_actors_movies_ids(self, movie_actors):
        """ Get IDs of movies that are in movie_actors rows which don't contain actors with 'N/A' values """
        return [movie_actor['movie_id'] for movie_actor in movie_actors]

    def get_movies(self):
        """ Get movies with valid actors """
        movies_ids = self.get_movie_actors_movies_ids(self.get_movie_actors())
        sql = "SELECT * FROM movies WHERE id IN (%s)" % ','.join('?' for _ in movies_ids)
        # Passing movies_ids to avoid sql injections (execute method will match list of '?' with movies_ids)
        return self.execute_sql(sql, movies_ids)

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
