import pydantic
from typing import List, Optional

from enums import SortField, SortOrder


class Actor(pydantic.BaseModel):
    id: int
    name: str = None


class Writer(pydantic.BaseModel):
    id: str
    name: str = None


class Movies(pydantic.BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class Movie(Movies):
    description: str
    writers: List[Writer] = None
    actors: List[Actor] = None
    genre: List[str]
    director: List[str] = None


class MoviesParams(pydantic.BaseModel):
    limit: int = 50
    page: int = 1
    sort: str = SortField.ID.value
    sort_order: str = SortOrder.ASC.value

    @pydantic.validator('limit')
    def validate_limit(cls, value):
        if value < 0:
            raise ValueError('limit cannot be negative')
        return value

    @pydantic.validator('page')
    def validate_page(cls, value):
        if value < 1:
            raise ValueError('page cannot be less then 1')
        return value

    @pydantic.validator('sort')
    def validate_sort(cls, value):
        if value not in SortField.to_list():
            raise ValueError('invalid sort field')
        return value

    @pydantic.validator('sort_order')
    def validate_sort_order(cls, value):
        if value not in SortOrder.to_list():
            raise ValueError('invalid sort_order order')
        return value
