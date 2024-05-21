from .serializers import (
    MovieSerializer
)
from .models import Movie
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response


class MovieViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Movie.objects.all()

    def list(self, request, *args, **kwargs):
        query_param = self.request.query_params.get('search')
        if query_param:
            queryset = Movie.objects.search(query_param)
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
