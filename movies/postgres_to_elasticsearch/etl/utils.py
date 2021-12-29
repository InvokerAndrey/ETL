from django.db.utils import OperationalError
from requests.exceptions import ConnectionError

import logging
from time import sleep
from functools import wraps


logger = logging.getLogger(__name__)


def coroutine(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        fn = func(self, *args, **kwargs)
        next(fn)
        return fn
    return inner


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_attempts=10):
    def wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            t = start_sleep_time
            exception = None
            for _ in range(max_attempts):
                try:
                    return func(self, *args, **kwargs)
                except (OperationalError, ConnectionError) as e:
                    exception = e
                    logger.exception(e)
                    sleep(t)
                    t = t * factor if t * factor < border_sleep_time else border_sleep_time
                    continue
            raise exception
        return inner
    return wrapper
