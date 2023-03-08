# -*- coding: utf-8 -*-
"""Serializers for the maplecroft.index module."""

# Standard Library
from collections import OrderedDict

# 3rd-party
from rest_framework import serializers

# Local
from . import services as service
from .models import Index


class IndexListSerializer(serializers.ModelSerializer):
    """Validate and serialize Index objects."""

    class Meta:  # noqa: D106
        model = Index
        fields = ['id', 'name']


class StatsSerializer(serializers.Serializer):
    """Validate and serialize aggregate statistics for IndexVersion."""

    id_ = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    mean = serializers.FloatField()
    min_ = serializers.FloatField()
    max_ = serializers.FloatField()
    median = serializers.FloatField()

    def get_fields(self):
        """Get registered fields."""
        fields = super().get_fields()
        # Single trailing underscore naming convention is used to avoid
        # conflicts with Python keywords. Here we strip any trailing
        # underscores, but maintain the original order of elements.
        renamed = OrderedDict((key.rstrip('_'), fields[key]) for key in fields)
        return renamed


class WindowSerializer(serializers.Serializer):
    """Validate and serialize a datetime range."""

    time_from = serializers.DateTimeField()
    time_to = serializers.DateTimeField()


class ScoredWindowSerializer(WindowSerializer):
    """Validate and serialize a scored window."""

    score = serializers.FloatField()


class WindowedDetailSerializer(serializers.ModelSerializer):
    """Validate and serialize an Index scored window."""

    averaged_scores = serializers.SerializerMethodField()

    class Meta:  # noqa: D106
        model = Index
        fields = ['id', 'name', 'averaged_scores']
        averaged_score_queryset_method = service.index_windowed_average

    def get_averaged_scores(self, obj):
        """Serialize the average IndexVersion.score over a given time period."""
        dtstart = self.context['time_from']
        dtend = self.context['time_to']
        get_windowed_average = getattr(self.Meta, 'averaged_score_queryset_method', {})
        return {
            'score': get_windowed_average(obj, dtstart, dtend)['score'],
            'time_from': dtstart,
            'time_to': dtend,
            }
