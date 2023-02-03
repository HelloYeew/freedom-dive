from django.core.management import BaseCommand

from apps.models import ScoreStore as OldScoreStore
from mirror.models import ScoreStore as NewScoreStore
from apps.models import PerformanceStore as OldPerformanceStore
from mirror.models import Performance as NewPerformanceStore
from apps.models import PerformanceByGraphStore as OldPerformanceByGraphStore
from mirror.models import PerformanceByGraph as NewPerformanceByGraphStore


class Command(BaseCommand):
    help = 'Transfer score from legacy store (apps) to new store (mirror)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Transferring score from legacy store to new store...'))
        for score in OldScoreStore.objects.all():
            try:
                NewScoreStore.objects.create(
                    id=score.id,
                    score_id=score.score_id,
                    user_id=score.user_id,
                    beatmap_id=score.beatmap_id,
                    created_at=score.date,
                    updated_at=score.date,
                    ruleset_short_name=score.ruleset_short_name,
                    passed=score.passed,
                    data=score.statistics,
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))
        for performance in OldPerformanceStore.objects.all():
            try:
                NewPerformanceStore.objects.create(
                    id=performance.id,
                    user_id=performance.user_id,
                    score_id=performance.score_id,
                    performance=performance.performance,
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))
        for performance in OldPerformanceByGraphStore.objects.all():
            try:
                NewPerformanceByGraphStore.objects.create(
                    id=performance.id,
                    user_id=performance.user_id,
                    score_id=performance.score_id,
                    performance=performance.performance,
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Finished transferring score from legacy store to new store'))
