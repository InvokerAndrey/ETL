from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('', views.FilmListView.as_view(), name='films'),
    path('etl/sqlite_to_postgres/', views.SqliteToPostgres.as_view(), name='sqlite_to_postgres'),
    path('<str:pk>', views.FilmDetailView.as_view(), name='film'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
