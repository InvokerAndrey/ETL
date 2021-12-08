import sqlite3


conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()


# С какими актёрами работал режиссер Jørgen Lerdam?
sql = """
    SELECT name FROM actors
    JOIN movie_actors ON actors.id = movie_actors.actor_id
    JOIN movies ON movies.id = movie_actors.movie_id
    WHERE movies.director LIKE '%Jørgen Lerdam%'
"""

cursor.execute(sql)
print(cursor.fetchall()) # [('Kaya Brüel',), ('Jesper Klein',), ('Søs Egelind',), ('Ditte Gråbøl',)]


# Кто из актеров снялся в большинстве фильмов?
sql = """
    SELECT name FROM actors
    JOIN movie_actors ON movie_actors.actor_id = actors.id
    GROUP BY actors.name
    HAVING COUNT(movie_actors.movie_id) = (
        SELECT MAX(movies_count) FROM (
            SELECT COUNT(movie_actors.movie_id) as movies_count FROM movie_actors
            JOIN actors ON movie_actors.actor_id = actors.id
            WHERE actors.name != 'N/A'
            GROUP BY actors.name
        )
    )
"""

cursor.execute(sql)
print(cursor.fetchall()) # [('Anthony Daniels',)]

conn.close()
