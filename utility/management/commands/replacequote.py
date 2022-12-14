from django.core.management import BaseCommand

from mirror.models import Beatmap
from utility.osu_database import get_connection


class Command(BaseCommand):
    help = 'Replace double single quote with one quote (Regressed in https://github.com/HelloYeew/freedom-dive/commit/d068ee3415f217879ac57da0f5d841862ad2f43d)'

    def handle(self, *args, **options):
        # Fix in mirror
        for beatmap in Beatmap.objects.all():
            beatmap.version = beatmap.version.replace("''", "'")
            beatmap.save()
            self.stdout.write(
                self.style.SUCCESS(f'Fixed {beatmap.version} in beatmapset {beatmap.beatmapset_id}'))
        # Fix in osu! database
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('USE osu')
        cursor.execute("UPDATE osu_beatmaps SET version = REPLACE(version, '''''', '''')")
        self.style.SUCCESS('Fixed in osu! database')
        self.style.SUCCESS('Fixed successfully!')
