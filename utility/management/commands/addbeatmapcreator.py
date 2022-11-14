from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from utility.osu_database import OsuUser, insert_user_to_database


class Command(BaseCommand):
    help = 'Adds a dummy beatmap creator to the osu! database'

    def add_arguments(self, parser):
        parser.add_argument('creator', type=str)

    def handle(self, *args, **options):
        creator = options['creator']
        creator_object = OsuUser(
            user_id=0,
            register_date=datetime.now(),
            username=creator,
            username_clean=creator,
            email=creator.lower() + '@helloyeew.dev',
            last_visit=datetime.now(),
            avatar="Dummy",
            signature="bruh",
            come_from="My home",
            country_acronym="JP",
            twitter="nonggummud",
            website="https://helloyeew.dev",
            occupation="Bot",
            interest="Beatmaps",
            playstyle=0,
            playmode=0,
            is_subscriber=False,
            subscription_expires=datetime.now()
        )
        try:
            insert_user_to_database(creator_object)
            self.stdout.write(self.style.SUCCESS('Successfully added beatmap creator "%s"' % creator))
        except Exception as e:
            raise CommandError('Failed to add beatmap creator "%s" due to "%s"' % (creator, e))
