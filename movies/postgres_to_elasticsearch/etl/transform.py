from movies.models import PersonRole


class Transform:
    def transform_movies(self, movies):
        transformed_movies = []
        for movie in movies:
            transformed_movies.append(self.transform_movie(movie))
        return transformed_movies

    def transform_movie(self, movie):
        actors = self._transform_person(movie, PersonRole.ACTOR) or None
        writers = self._transform_person(movie, PersonRole.WRITER) or None
        directors = self._transform_person(movie, PersonRole.DIRECTOR) or None
        actors_names = ', '.join([actor['name'] for actor in actors]) if actors else None
        writers_names = ', '.join([writer['name'] for writer in writers]) if writers else None
        directors_names = ', '.join([director['name'] for director in directors]) if directors else None
        transformed_movie = {
            'id': str(movie.id),
            'title': movie.title,
            'description': movie.description,
            'imdb_rating': movie.rating,
            'genre': ', '.join([genre.name for genre in movie.genres.all()]),
            'actors': actors,
            'writers': writers,
            'director': directors_names,
            'actors_names': actors_names,
            'writers_names': writers_names
        }
        return transformed_movie

    def _transform_person(self, movie, role):
        return [
            {
                'id': str(person.id),
                'name': (person.first_name + ' ' + person.last_name).strip()
            }
            for person in movie.person.filter(role=role)
        ]
