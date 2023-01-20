from django.core.management import BaseCommand

from utility.seeder.seeder import seed_country


class Command(BaseCommand):
    help = 'Seed country data to Country table. More info see seeder/seeder.py in utility apps'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Running seed_country'))
        seed_country()
        self.stdout.write(self.style.SUCCESS(f'Finished seed_country!'))
