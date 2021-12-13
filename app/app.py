from flask import Flask, request
from flask_cors import CORS
import pydantic

import requests
import json

import models
import utils


app = Flask('movies_service')
CORS(app)


@app.route('/api/test', methods=['GET'])
def test():
    try:
        params = models.MoviesParams(**dict(request.args))
    except pydantic.ValidationError as e:
        return e.json()
    return params.json()


@app.route('/api/movies', methods=['GET'])
def movies_list():
    try:
        params = models.MoviesParams(**dict(request.args))
        start = params.limit * (params.page - 1)

        data = json.dumps({
            'sort': [
                {params.sort: {'order': params.sort_order}}
            ],
            "from": start,
            "size": params.limit,
        })
        response = requests.get(
            'http://127.0.0.1:9200/movies/_search/',
            data=data,
            headers={'Content-Type': 'application/x-ndjson'}
        )
        return utils.get_movies_json_response(response, params)
    except pydantic.ValidationError as e:
        return e.json(), 422


@app.route('/api/movies/<movie_id>', methods=['GET'])
def movie_details(movie_id):
    data = json.dumps({
        "query": {
            "match": {
              "_id": movie_id
            }
        }
    })
    response = requests.get(
        'http://127.0.0.1:9200/movies/_search/',
        data=data,
        headers={'Content-Type': 'application/x-ndjson'}
    )
    if not response.json()['hits']['hits']:
        return 'movie not found', 404
    return utils.get_movie_json_response(response)


if __name__ == '__main__':
    app.run(port=8000)
