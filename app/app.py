from flask import Flask, request, jsonify
from flask_cors import CORS
import pydantic

import requests
import json

import models
import utils


app = Flask('movies_service')
CORS(app)


@app.route('/api/movies', methods=['GET'], strict_slashes=False)
def movies_list():
    try:
        params = models.MoviesParams(**dict(request.args))
        start = params.limit * (params.page - 1)
        data = {
           "from": start,
           "size": params.limit,
            "sort": [
                {params.sort: {"order": params.sort_order}}
            ],
        }
        if params.search:
            data["query"] = {
                "multi_match": {
                    "query": params.search,
                    "fuzziness": "auto",
                    "fields": [
                        "title^5",
                        "description^4",
                        "genre^3",
                        "actors_names^3",
                        "writers_names^2",
                        "director"
                    ]
                },
            }
        response = requests.get(
            'http://127.0.0.1:9200/movies/_search/',
            data=json.dumps(data),
            headers={'Content-Type': 'application/x-ndjson'}
        )
        return jsonify(utils.get_movies_json_response(response, params))
    except pydantic.ValidationError as e:
        return e.json(), 422


@app.route('/api/movies/<string:movie_id>', methods=['GET'])
def movie_details(movie_id):
    try:
        data = json.dumps({
            "query": {
                "match": {
                  "id": movie_id
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
    except pydantic.ValidationError as e:
        return e.json(), 200


if __name__ == '__main__':
    app.run(port=8000)
