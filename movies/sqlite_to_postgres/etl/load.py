from django.db.utils import IntegrityError

from movies.models import Filmwork, Genre, Person, FilmworkType, PersonRole


class Load:
    def save_genres(self, genres):
        try:
            return Genre.objects.bulk_create(
                [Genre(name=genre) for genre in genres]
            )
        except IntegrityError:
            pass

    def save_actors(self, actors):
        return Person.objects.bulk_create(
            [
                Person(
                    first_name=actor.split(maxsplit=1)[0],
                    last_name=actor.split(maxsplit=1)[1] if len(actor.split(maxsplit=1)) > 1 else '',
                    role=PersonRole.ACTOR
                )
                for actor in actors.keys()
            ]
        )

    def save_writers(self, writers):
        return Person.objects.bulk_create(
            [
                Person(
                    first_name=writer.split(maxsplit=1)[0],
                    last_name=writer.split(maxsplit=1)[1] if len(writer.split(maxsplit=1)) > 1 else '',
                    role=PersonRole.WRITER
                )
                for writer in writers.keys()
            ]
        )

    def save_directors(self, directors):
        return Person.objects.bulk_create(
            [
                Person(
                    first_name=director.split(maxsplit=1)[0],
                    last_name=director.split(maxsplit=1)[1] if len(director.split(maxsplit=1)) > 1 else '',
                    role=PersonRole.DIRECTOR
                )
                for director in directors.keys()
            ]
        )

    def save_movies(self, movies):
        pass
