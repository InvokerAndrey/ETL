class Movies:
    def __init__(self, response, limit):
        self.es_response = response
        self.limit = limit

    def get_response(self):
        return [
            {
                'id': self.es_response.json()['hits']['hits'][i]['_source']['id'],
                'title': self.es_response.json()['hits']['hits'][i]['_source']['title'],
                'imdb_rating': self.es_response.json()['hits']['hits'][i]['_source']['imdb_rating'],
            }
            for i in range(self.limit)
        ]
