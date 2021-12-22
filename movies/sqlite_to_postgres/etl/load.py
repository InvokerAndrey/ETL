from movies.models import Filmwork, Genre, Person, FilmworkType


class Load:
    def save_genres(self, genres):
        return Genre.objects.bulk_create(
                [Genre(name=genre) for genre in genres],
                ignore_conflicts=True
            )

    def save_person(self, person, role):
        person_objects = []
        existing_persons = Person.objects.values('first_name', 'last_name').filter(role=role)
        for person_name in person.keys():
            split_name = person_name.split(maxsplit=1)
            first_name = split_name[0]
            last_name = split_name[1] if len(split_name) > 1 else ''
            # check if person exists
            for existing_person in existing_persons:
                if first_name == existing_person['first_name'] and last_name == existing_person['last_name']:
                    break
            else:
                person_obj = Person(
                    first_name=first_name,
                    last_name=last_name,
                    role=role
                )
                person_objects.append(person_obj)
        return Person.objects.bulk_create(person_objects)

    def save_movies(self, movies):
        for movie in movies:
            film = Filmwork(
                    title=movie['title'],
                    description=movie['description'],
                    creation_date=None,
                    certificate=None,
                    rating=movie['rating'],
                    type=FilmworkType.MOVIE
                )
            film.save()

            actor_ids = self._get_ids(movie['actors'])
            writer_ids = self._get_ids(movie['writers'])
            director_ids = self._get_ids(movie['directors'])

            film.genres.set([genre.id for genre in movie['genres']])
            film.person.set(actor_ids + writer_ids + director_ids)

    def _get_ids(self, list_of_qs):
        ids = []
        for person in list_of_qs:
            if not person:
                continue
            ids.append(person.id)
        return ids
