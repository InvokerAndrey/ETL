import json
from typing import List
from collections import defaultdict


class Transform:
    def validate_genres(self, genres_str: str) -> set:
        """
        :param genres_str: 'Action, Adventure, Action, Sci-Fi, ...'
        :return: {'Action', 'Adventure', 'Sci-Fi', ...}
        """
        return set(genres_str.split(', '))

    def validate_actors(self, raw_actors: List[dict]):
        actors = defaultdict(set)
        for raw_actors in raw_actors:
            actors[raw_actors['name']].add(raw_actors['movie_id'])
        return actors

    def validate_writers(self, raw_writers: List[dict], raw_movie_writers: List[dict]):
        """
        :param raw_writers: [
            {
                'id': writer.id,
                'name': writer.name
            }, ...
        ]
        :param raw_movie_writers: [
            {
                'movie_id': movie.id,
                'writers': "[{'id': writer.id}, ...]"
            }
        ]
        :return: { writer_name: {movie_id, ...} }
        """
        writers = defaultdict(set)
        for raw_writer in raw_writers:
            for raw_movie_writer in raw_movie_writers:
                if not raw_movie_writer['writers']:
                    continue
                for raw_writer_id in json.loads(raw_movie_writer['writers']):
                    name = raw_writer['name']
                    writers[name] |= set()
                    if raw_writer['id'] == raw_writer_id['id']:
                        writers[name].add(raw_movie_writer['movie_id'])
        return writers

    def validate_directors(self, raw_directors):
        """
        :param raw_directors: [
            {
                'movie_id': ,
                'director': ['director.name',...],
            }
        ]
        :return:
        """
        directors = defaultdict(set)
        for raw_director in raw_directors:
            for name in raw_director['director'].split(', '):
                directors[name].add(raw_director['movie_id'])
        return directors
