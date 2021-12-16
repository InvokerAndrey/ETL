from django.contrib import admin

from .models import Filmwork, Person, Genre


class PersonAdmin(admin.ModelAdmin):
    list_filter = ('role',)


class FilmworkAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating')
    # фильтрация в списке
    list_filter = ('type',)
    # поиск по полям
    search_fields = ('title', 'description', 'id')
    # порядок следования полей в форме создания/редактирования
    fields = ('title', 'type', 'description', 'creation_date', 'certificate', 'rating', 'genres', 'person')


admin.site.register(Filmwork, FilmworkAdmin)
admin.site.register(Genre)
admin.site.register(Person, PersonAdmin)
