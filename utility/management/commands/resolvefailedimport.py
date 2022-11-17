from django.core.management import BaseCommand

from utility.management.commands.bulkimportbeatmap import import_beatmapset


class Command(BaseCommand):
    help = 'Resolve failed imports by reimporting beatmapsets from failed.txt list'

    def handle(self, *args, **options):
        try:
            with open('failed.txt', 'r') as f:
                # create a list of beatmapset ids from failed.txt with remove duplicates and
                # string that cannot be converted to int
                beatmapset_ids = list(set([int(line) for line in f.readlines() if line.strip().isdigit()]))
                # clean up failed.txt
                with open('failed.txt', 'w') as f:
                    f.write('')
                self.stdout.write(self.style.SUCCESS(f'Found {len(beatmapset_ids)} beatmapset ids in failed.txt'))
                import_beatmapset(self, beatmapset_ids)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('failed.txt not found'))
