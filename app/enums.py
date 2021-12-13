import enum


class BaseEnum(enum.Enum):
    @classmethod
    def to_list(cls):
        return [field.value for field in cls]


class SortField(BaseEnum):
    ID = 'id'
    TITLE = 'title'
    IMDB_RATING = 'imdb_rating'


class SortOrder(BaseEnum):
    ASC = 'asc'
    DESC = 'desc'
