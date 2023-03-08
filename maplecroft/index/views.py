# -*- coding: utf-8 -*-
"""REST API views for the maplecroft.index module."""

# 3rd-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

# Local
from . import services as service
from .serializers import IndexListSerializer
from .serializers import StatsSerializer
from .serializers import WindowedDetailSerializer
from .serializers import WindowSerializer


class IndexListView(generics.ListAPIView):
    """Return all indices.

    Results may be filtered by the primary key `id`.
    Results may be ordered by the `name` field.
    """

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['id']
    ordering = 'id'
    ordering_fields = ['name']
    queryset = service.index_queryset()
    serializer_class = IndexListSerializer


class StatsListView(generics.ListAPIView):
    """Return the maximum, minimum, mean and median for each index."""

    queryset = service.index_stats_queryset()
    serializer_class = StatsSerializer


class WindowedDetailView(generics.RetrieveAPIView):
    """Return the mean score for a given index and period."""

    filterset_fields = ['id']
    query_params_serializer_class = WindowSerializer
    queryset = service.index_queryset()
    serializer_class = WindowedDetailSerializer

    def get_valid_query_params(self, request):
        """Return validated and deserialized request query-parameters."""
        params = self.query_params_serializer_class(data=request.query_params)
        params.is_valid(raise_exception=True)
        return params.data

    def get_serializer(self, *args, **kwargs):
        """Return a prepared serializer instance."""
        kwargs['context'] = self.get_serializer_context()
        kwargs['context'].update(self.get_valid_query_params(self.request))
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)
