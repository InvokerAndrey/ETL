import logging
from time import sleep
from functools import wraps

from psycopg2 import OperationalError


logger = logging.getLogger(__name__)


def coroutine(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        fn = func(self, *args, **kwargs)
        next(fn)
        return fn
    return inner


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            t = start_sleep_time * 2 ** factor if start_sleep_time * 2 ** factor < border_sleep_time else border_sleep_time
            try:
                return func(self, *args, **kwargs)
            except OperationalError as e:
                logger.exception(e)
                sleep(t)
                return func(self, *args, **kwargs)
        return inner
    return wrapper
