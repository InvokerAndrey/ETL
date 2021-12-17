from rest_framework import serializers

from .models import Filmwork, PersonRole


class FilmSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField(read_only=True)
    actors = serializers.SerializerMethodField(read_only=True)
    directors = serializers.SerializerMethodField(read_only=True)
    writers = serializers.SerializerMethodField(read_only=True)

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_actors(self, obj):
        return [(str(actor.first_name) + ' ' + str(actor.last_name)).strip() for actor in obj.person.all() if actor.role == PersonRole.ACTOR and actor.first_name is not None]

    def get_directors(self, obj):
        return [(str(director.first_name) + ' ' + str(director.last_name)).strip() for director in obj.person.all() if director.role == PersonRole.DIRECTOR]

    def get_writers(self, obj):
        return [(str(writer.first_name) + ' ' + str(writer.last_name)).strip() for writer in obj.person.all() if writer.role == PersonRole.WRITER]

    class Meta:
        model = Filmwork
        fields = [
            'id', 'title', 'description', 'creation_date', 'rating',
            'type', 'genres', 'actors', 'directors', 'writers'
        ]
