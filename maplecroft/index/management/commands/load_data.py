import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.utils import timezone
from tqdm import tqdm

from maplecroft.index.models import Index, IndexVersion


class Command(BaseCommand):

    VERSIONS_COUNT = 100000

    @atomic
    def handle(self, *args, **options):
        indices = ['Child Labour', 'Air Quality', 'Corruption', 'Forced Labour', 'Governance']

        now = timezone.now()

        Index.objects.all()
        IndexVersion.objects.all()

        for index in tqdm(indices, total=len(indices)):
            index = Index(name=index)
            index.save()

            versions = []

            for version_number in range(0, self.VERSIONS_COUNT):
                score = random.uniform(0,10)
                timestamp = now + timedelta(minutes=version_number)
                versions.append(
                    IndexVersion(
                        score=score,
                        timestamp=timestamp,
                        index=index,
                        version=version_number
                    )
                )
            IndexVersion.objects.bulk_create(versions)