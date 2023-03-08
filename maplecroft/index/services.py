# -*- coding: utf-8 -*-
"""Helpers and utilities exposed within the maplecroft.index module."""

# Django
from django.db.models import Aggregate
from django.db.models import Avg
from django.db.models import FloatField
from django.db.models import Max
from django.db.models import Min

# Local
from .models import Index


class Median(Aggregate):
    """Provide the missing median aggregation for Django ORM."""

    function = 'PERCENTILE_CONT'
    name = 'median'
    output_field = FloatField()
    template = '%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)'


def index_queryset():
    """Abstract the base queryset."""
    return Index.objects.all()


def index_stats_queryset():
    """Abstract the aggregate stats queryset for indices."""
    queryset = index_queryset()
    lookup_field = 'indexversion__score'
    aggregations = {
        'max': Max(lookup_field),
        'mean': Avg(lookup_field),
        'median': Median(lookup_field),
        'min': Min(lookup_field),
    }
    return queryset.annotate(**aggregations)


def index_windowed_average(instance, dtstart, dtend):
    """Return average score for a signle Index over a given period."""
    windowed = instance.indexversion_set.filter(
        timestamp__gte=dtstart,
        timestamp__lte=dtend,
        )
    return windowed.aggregate(score=Avg('score'))
