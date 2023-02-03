from django.core.management import BaseCommand

from mirror.models import ScoreStore
from utility.ruleset.utils import get_ruleset_id


class Command(BaseCommand):
    help = 'Update ruleset ID to very far from legacy ruleset ID'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Transferring ruleset ID to a new one'))
        for score in ScoreStore.objects.all():
            try:
                score.data['ruleset_id'] = get_ruleset_id(score.ruleset_short_name)
                print("Updating score ID: " + score.score_id + " with ruleset ID: " + str(score.data['ruleset_id']))
                print(score.data)
                score.save()
            except Exception as e:
                print("Error updating score ID: " + score.score_id)
                print(e)
        self.stdout.write(self.style.SUCCESS(f'Finished transferring ruleset ID to a new one'))
