from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Filmwork
from .serializers import FilmSerializer


class Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(dict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('prev', self.get_previous_link()),
            ('next', self.get_next_link()),
            ('result', data),
        ]))


class FilmListView(APIView):
    def get(self, request, format=None):
        paginator = Pagination()
        film_qs = Filmwork.objects.all()
        page = paginator.paginate_queryset(film_qs, request)
        serializer = FilmSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SqliteToPostgres(APIView):
    def get(self, request, format=None):
        from .sqlite_to_postgres.pipeline import PipelineETL
        PipelineETL().run()
        return HttpResponseRedirect(reverse('films'))


class FilmDetailView(APIView):
    def _get_film(self, pk):
        return get_object_or_404(Filmwork, pk=pk)

    def get(self, request, pk, format=None):
        film = self._get_film(pk)
        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)
