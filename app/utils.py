import models


def get_movies_json_response(response, params):
    for i in range(params.limit):
        movies = models.Movies(
            id=response.json()['hits']['hits'][i]['_source']['id'],
            title=response.json()['hits']['hits'][i]['_source']['title'],
            imdb_rating=response.json()['hits']['hits'][i]['_source']['imdb_rating']
        )
        return movies.json()


def get_movie_json_response(response):
    director = response.json()['hits']['hits'][0]['_source']['director']
    director = director.split(', ') if director else None

    movie = models.Movie(
        id=response.json()['hits']['hits'][0]['_source']['id'],
        title=response.json()['hits']['hits'][0]['_source']['title'],
        description=response.json()['hits']['hits'][0]['_source']['description'],
        imdb_rating=response.json()['hits']['hits'][0]['_source']['imdb_rating'],
        writers=response.json()['hits']['hits'][0]['_source']['writers'],
        actors=response.json()['hits']['hits'][0]['_source']['actors'],
        genre=response.json()['hits']['hits'][0]['_source']['genre'].split(', '),
        director=director
    )
    return movie.json()
