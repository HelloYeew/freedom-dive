from django.db import connection as db_connection
from django.core.management import BaseCommand

from mirror.models import Beatmap
from utility.osu_database import get_connection


class Command(BaseCommand):
    help = 'Replace double single quote with one quote (Regressed in https://github.com/HelloYeew/freedom-dive/commit/d068ee3415f217879ac57da0f5d841862ad2f43d)'

    def handle(self, *args, **options):
        # Fix in mirror
        # Use raw SQL because memory usage is too high
        db_connection.cursor().execute("UPDATE mirror_beatmap SET version = REPLACE(version, '''''', '''')")
        self.stdout.write(self.style.SUCCESS(f'Fixed in mirror!'))
        # Fix in osu! database
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('USE osu')
        cursor.execute("UPDATE osu_beatmaps SET version = REPLACE(version, '''''', '''')")
        self.stdout.write(self.style.SUCCESS('Fixed in osu! database'))
        self.stdout.write(self.style.SUCCESS('Fixed successfully!'))
