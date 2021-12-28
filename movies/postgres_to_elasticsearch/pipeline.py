import logging

from .etl.extract import Extract
from .etl.transform import Transform
from .etl.load import Load
from .etl.state import State
from .etl.utils import coroutine


logger = logging.getLogger(__name__)


class PipelineETL:
    def __init__(self):
        self.extract = Extract()
        self.transform = Transform()
        self.load = Load()
        self.state = State('storage.txt')

    def _extract_movies(self, transformer, **kwargs):
        limit = 100
        offset_number = self.state.get_state()
        offset = offset_number or 0
        logger.info(f'Starting from {offset}')
        try:
            while True:
                extract_function = getattr(self.extract, kwargs['extract_function'])
                function_args = kwargs['function_args']
                movies = extract_function(*function_args, limit=limit, offset=offset)
                if not movies:
                    break
                transformer.send(movies)
                offset += limit
        except Exception as e:
            logger.error('Something went wrong!!!!!!!!!!!!!!!')
            logger.exception(e)
            self.state.set_state(offset)
        else:
            logger.info('Clear storage')
            self.state.clear_state()

    @coroutine
    def _transform_movies(self, loader):
        while True:
            movies = (yield)
            transformed_movies = self.transform.transform_movies(movies)
            loader.send(transformed_movies)

    @coroutine
    def _load_movies(self):
        while True:
            movies = (yield)
            self.load.load_movies(movies)

    @coroutine
    def _update_movies_by_genre(self):
        while True:
            movies = (yield)
            logger.info(self.load.update_genre_in_movies(movies).content)

    @coroutine
    def _update_movies_by_person(self):
        while True:
            movies = (yield)
            logger.info(self.load.update_person_in_movies(movies).content)


class PipelineMovies(PipelineETL):
    def _transform_movie(self, movie):
        return self.transform.transform_movie(movie)

    def _update_movie(self, movie):
        logger.info(self.load.update_movie(movie).content)

    def _load_movie(self, movie):
        logger.info(self.load.load_movie(movie).content)

    def migrate_all_movies(self):
        logger.info('Start migrating all data')
        loader = self._load_movies()
        transformer = self._transform_movies(loader)
        self._extract_movies(transformer, extract_function='get_movies', function_args=[])
        logger.info('End migrating all data')

    def migrate_movie_updates(self, movie):
        logger.info('Start updating movie data')
        self._update_movie(self._transform_movie(movie))

    def migrate_new_movie(self, movie):
        logger.info('Start creating new movie')
        self._load_movie(self._transform_movie(movie))

    def delete_movie(self, movie_id):
        logger.info(f'Deleting movie {movie_id}')
        logger.info(self.load.delete_movie(movie_id).content)


class PipelineGenre(PipelineETL):
    def migrate_genre_updates(self, genre):
        logger.info('Start migrating genre data')
        loader = self._update_movies_by_genre()
        transformer = self._transform_movies(loader)
        self._extract_movies(transformer, extract_function='get_movies_by_genre', function_args=[genre])

    def delete_genre_from_movies(self, movies_ids):
        logger.info('Start deleting genre from movies')
        loader = self._update_movies_by_genre()
        transformer = self._transform_movies(loader)
        self._extract_movies(transformer, extract_function='get_movies_by_ids', function_args=[movies_ids])


class PipelinePerson(PipelineETL):
    def migrate_person_updates(self, person):
        logger.info('Start migrating person data')
        loader = self._update_movies_by_person()
        transformer = self._transform_movies(loader)
        self._extract_movies(transformer, extract_function='get_movies_by_person', function_args=[person])

    def delete_person_from_movies(self, movies_ids):
        logger.info('Start deleting person from movies')
        loader = self._update_movies_by_person()
        transformer = self._transform_movies(loader)
        self._extract_movies(transformer, extract_function='get_movies_by_ids', function_args=[movies_ids])
