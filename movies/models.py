from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.core.validators import MinValueValidator

import uuid


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('название'), max_length=255, unique=True)
    description = models.TextField(_('описание'), blank=True, null=True)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')
        app_label = 'movies'

    def __str__(self):
        return self.name


class PersonRole(models.TextChoices):
    ACTOR = 'actor', _('актер')
    WRITER = 'writer', _('сценарист')
    DIRECTOR = 'director', _('режиссер')


class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('имя'), max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(_('фамилия'), max_length=255, blank=True, null=True, default='')
    role = models.CharField(_('роль'), max_length=20, choices=PersonRole.choices)

    @property
    def name(self):
        return self.first_name + self.last_name

    class Meta:
        verbose_name = _('человек')
        verbose_name_plural = _('люди')
        app_label = 'movies'

    def __str__(self):
        return f'{self.role}: {self.first_name} {self.last_name}'


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('фильм')
    TV_SHOW = 'tv_show', _('сериал')


class Filmwork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True, null=True)
    creation_date = models.DateField(_('дата создания фильма'), blank=True, null=True)
    certificate = models.TextField(_('сертификат'), blank=True, null=True)
    file_path = models.FileField(_('файл'), upload_to='film_works/', blank=True, null=True),
    rating = models.FloatField(_('рейтинг'), validators=[MinValueValidator(0)], blank=True, null=True)
    type = models.CharField(_('тип'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre)
    person = models.ManyToManyField(Person, blank=True, null=True)

    class Meta:
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')
        app_label = 'movies'

    def __str__(self):
        return self.title
