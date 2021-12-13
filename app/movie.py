class Movie:
    def __init__(self, response):
        self.es_response = response

    def get_response(self):
        _id = self.es_response.json()['hits']['hits'][0]['_source']['id']
        title = self.es_response.json()['hits']['hits'][0]['_source']['title']
        description = self.es_response.json()['hits']['hits'][0]['_source']['description']
        imdb_rating = self.es_response.json()['hits']['hits'][0]['_source']['imdb_rating']
        writers = self.es_response.json()['hits']['hits'][0]['_source']['writers']
        actors = self.es_response.json()['hits']['hits'][0]['_source']['actors']
        genre = self.es_response.json()['hits']['hits'][0]['_source']['genre']
        if genre:
            genre = genre.split(', ')
        director = self.es_response.json()['hits']['hits'][0]['_source']['director']
        if director:
            director = director.split(', ')
        return {
            'id': _id,
            'title': title,
            'description': description,
            'imdb_rating': imdb_rating,
            'writers': writers,
            'actors': actors,
            'genre': genre,
            'director': director,
        }