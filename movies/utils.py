from .models import *


def print_films():
    films = Filmwork.objects.all()
    for film in films:
        print("=" * 50)
        print('title:', film.title)
        print('-' * 50)
        print('description:', film.description and film.description[:40], '...')
        print('-' * 50)
        print('creation_date:', film.creation_date)
        print('-' * 50)
        print('certificate:', film.certificate)
        print('-' * 50)
        print('file_path:', film.file_path)
        print('-' * 50)
        print('rating:', film.rating)
        print('-' * 50)
        print('type:', film.type)
        print('-' * 50)
        print('genres:')
        for genre in film.genres.all():
            print(genre.name, sep=', ')
        print('-' * 50)
        print('guys:')
        for person in film.person.all():
            print(person.role, ':', person.first_name)
            print('*' * 10)
