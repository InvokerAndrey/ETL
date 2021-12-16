import models


def get_movies_json_response(response, params):
    movies = []
    try:
        for i in range(params.limit):
            movies.append(models.Movies(
                **response.json()['hits']['hits'][i]['_source']
            ).json())
        return movies
    except IndexError:
        return movies


def get_movie_json_response(response):
    movie = models.Movie(
        **response.json()['hits']['hits'][0]['_source'],
    )
    return movie.json()
