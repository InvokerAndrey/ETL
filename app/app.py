from flask import Flask, request, jsonify
from flask_cors import CORS

import requests
import json


app = Flask('movies_service')
CORS(app)


@app.route('/api/movies')
def movies_list():
    try:
        try:
            limit = int(request.args.get('limit')) if request.args.get('limit') else 50

        except ValueError:
            raise ValueError({
                'loc': [
                    'query',
                    'limit'
                    ],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'
            })
        try:
            page = int(request.args.get('page')) if request.args.get('page') else 1
        except ValueError:
            raise ValueError({
                'loc': [
                    'query',
                    'page'
                    ],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'
            })
        sort = request.args.get('sort') if request.args.get('sort') else 'id'
        sort_order = request.args.get('sort_order') if request.args.get('sort_order') else 'asc'
        if sort not in ('id', 'title', 'imdb_rating'):
            raise ValueError({
                'loc': [
                    'query',
                    'sort'
                    ],
                'msg': 'value is not a valid field',
                'type': 'choice_error.field'
            })
        if sort_order not in ('asc', 'desc'):
            raise ValueError({
                'loc': [
                    'query',
                    'sort_order'
                    ],
                'msg': 'value is not a valid parameter',
                'type': 'choice_error.parameter'
            })
        start = limit * (page - 1)

        data = json.dumps({
            'sort': [
                {sort: {'order': sort_order}}
            ],
            "from": start,
            "size": limit,
        })
        params = {
            'pretty': 'true',
        }
        response = requests.get(
            'http://127.0.0.1:9200/movies/_search/',
            params=params,
            data=data,
            headers={'Content-Type': 'application/x-ndjson'}
        )
        result = [
            {
                'id': response.json()['hits']['hits'][i]['_source']['id'],
                'title': response.json()['hits']['hits'][i]['_source']['title'],
                'imdb_rating': response.json()['hits']['hits'][i]['_source']['imdb_rating'],
            }
            for i in range(limit)
        ]
        return jsonify(result)
    except ValueError as e:
        return jsonify(str(e)), 422
