import pydantic

from typing import List
import datetime


class Movie(pydantic.BaseModel):
    title: str
    description: str = None
    creation_date: datetime.datetime = None
    certificate: str = None
    file_path: str = None
    rating: float = None
    type: str
    genres: List[str]
    person: List[str] = None


class Genre(pydantic.BaseModel):
    name: str
    description: str = None


class Person(pydantic.BaseModel):
    id: str
    first_name: str = None
    last_name: str = None
    role: str
