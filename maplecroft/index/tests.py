# -*- coding: utf-8 -*-

# Standard Library
import random

# Django
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Min
from django.test import TestCase
from django.utils import timezone

# Local
from .models import Index
from .models import IndexVersion
from .services import Median
from .services import index_queryset
from .services import index_stats_queryset
from .services import index_windowed_average


class TestIndexQueryset(TestCase):

    def setUp(self):
        self.instance = Index.objects.create(name='index1')

    def test_function_returns_expected_queryset(self):
        expected = self.instance.name

        actual = index_queryset()[0].name

        self.assertEqual(actual, expected)


class TestIndexStatsQueryset(TestCase):

    def setUp(self):
        self.now = timezone.now()
        self.versions_count = 10
        index = Index.objects.create(name='index1')
        versions = []

        for version_number in range(0, self.versions_count):
            score = random.uniform(1, 10)  # noqa: S311
            timestamp = self.now + timezone.timedelta(minutes=version_number)
            indexversion = IndexVersion(
                score=score,
                timestamp=timestamp,
                index=index,
                version=version_number,
                )
            versions.append(indexversion)
        IndexVersion.objects.bulk_create(versions)

    def test_function_returns_expected_max(self):
        expected = IndexVersion.objects.all().aggregate(value=Max('score'))['value']

        actual = index_stats_queryset()[0].max

        self.assertEqual(actual, expected)
        self.assertTrue(10 >= actual >= 1)

    def test_function_returns_expected_min(self):
        expected = IndexVersion.objects.all().aggregate(value=Min('score'))['value']

        actual = index_stats_queryset()[0].min

        self.assertEqual(actual, expected)
        self.assertTrue(10 >= actual >= 1)

    def test_function_returns_expected_mean(self):
        expected = IndexVersion.objects.all().aggregate(value=Avg('score'))['value']

        actual = index_stats_queryset()[0].mean

        self.assertEqual(actual, expected)
        self.assertTrue(10 >= actual >= 1)

    def test_function_returns_expected_median(self):
        expected = IndexVersion.objects.all().aggregate(value=Median('score'))['value']

        actual = index_stats_queryset()[0].median

        self.assertEqual(actual, expected)
        self.assertTrue(10 >= actual >= 1)


class TestIndexWindowedAverage(TestCase):

    def setUp(self):
        self.now = timezone.now()
        self.versions_count = 10
        self.index = Index.objects.create(name='index1')
        versions = []

        for version_number in range(0, self.versions_count):
            score = random.uniform(1, 10)  # noqa: S311
            timestamp = self.now + timezone.timedelta(minutes=version_number)
            indexversion = IndexVersion(
                score=score,
                timestamp=timestamp,
                index=self.index,
                version=version_number,
                )
            versions.append(indexversion)
        IndexVersion.objects.bulk_create(versions)

    def test_function_returns_expected_dictionary(self):
        dtstart = self.now + timezone.timedelta(minutes=1)
        dtend = self.now + timezone.timedelta(minutes=6)

        expected = IndexVersion.objects.filter(
            timestamp__gte=dtstart,
            timestamp__lte=dtend,
            ).aggregate(score=Avg('score'))

        actual = index_windowed_average(self.index, dtstart, dtend)

        self.assertEqual(actual, expected)
