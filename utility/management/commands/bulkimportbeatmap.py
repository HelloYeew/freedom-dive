import time
import traceback

import requests
from decouple import config
from django.core.management import BaseCommand
from mysql.connector import InterfaceError, IntegrityError

from mirror.utils import import_beatmapset_to_mirror, import_beatmap_to_mirror
from utility.osu_database import get_beatmapset_by_id, import_beatmapset_from_api, update_beatmapset_from_api, \
    get_beatmap_by_beatmapset
from utility.s3.utils import get_s3_client

BEATMAP_CREATOR_DUMMY_ID = int(config('BEATMAP_CREATOR_ID', default='10'))
S3_BUCKET_NAME = config('S3_BUCKET_NAME', default='')


class Command(BaseCommand):
    help = 'Import a beatmapset from osu! API from given range'

    def add_arguments(self, parser):
        parser.add_argument('start', type=int)
        parser.add_argument('end', type=int)

    def handle(self, *args, **options):
        start = options['start']
        end = options['end']
        # Create list of beatmapset ids
        beatmapset_id_list = list(range(start, end + 1))
        import_beatmapset(self, beatmapset_id_list)


def import_beatmapset(self: BaseCommand, id_list: list[int], failed_file_path: str = 'failed'):
    s3_client = get_s3_client()
    # create text file for store failed beatmapset id
    failed_file = open(f"{failed_file_path}.txt", "w")
    # add ---------- to separate each import
    failed_file.write("----------\n")
    # loop through beatmapset id
    for i in id_list:
        try:
            # find beatmapset by id in osu! database
            beatmapset = get_beatmapset_by_id(i)
            if beatmapset:
                self.stdout.write(
                    self.style.SUCCESS('Beatmapset "%s" already exists in database, updating...' % beatmapset.title))
                update_beatmapset_from_api(i)
                import_beatmapset_to_mirror(beatmapset)
                beatmapset = get_beatmap_by_beatmapset(i)
                for beatmap in beatmapset:
                    import_beatmap_to_mirror(beatmap)
                print(f"Beatmapset {i} has been updated.")
            else:
                self.stdout.write(self.style.SUCCESS('Beatmapset with id "%s" not found in database, importing...' % i))
                import_beatmapset_from_api(i)
                self.stdout.write(
                    self.style.SUCCESS(f"Beatmapset {i} has been imported, importing to mirror database..."))
                beatmapset = get_beatmapset_by_id(i)
                if beatmapset is not None:
                    import_beatmapset_to_mirror(beatmapset)
                    beatmapset = get_beatmap_by_beatmapset(i)
                    for beatmap in beatmapset:
                        import_beatmap_to_mirror(beatmap)
        except Exception as e:
            self.stdout.write(self.style.ERROR('Error importing beatmapset with id "%s": %s' % (i, e)))
            # Ignored InterfaceError and IntegrityError, only log when other error occured
            if not isinstance(e, (InterfaceError, IntegrityError)):
                failed_file.write(str(i) + "\n")
                traceback.print_exc()
        try:
            card_pic = requests.get(f"https://assets.ppy.sh/beatmaps/{i}/covers/card.jpg")
            list_pic = requests.get(f"https://assets.ppy.sh/beatmaps/{i}/covers/list.jpg")
            cover_pic = requests.get(f"https://assets.ppy.sh/beatmaps/{i}/covers/cover.jpg")
            thumbnail_pic = requests.get(f"https://b.ppy.sh/thumb/{i}l.jpg")
            if ("Access Denied" or "Not Found") not in str(card_pic.content) and card_pic.status_code == 200:
                print("Uploading card pic...")
                s3_client.put_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=f"card/{i}.jpg",
                    Body=card_pic.content,
                    ContentType="image/jpeg",
                    ACL="public-read",
                    CacheControl="max-age=31536000"
                )
            if ("Access Denied" or "Not Found") not in str(list_pic.content) and list_pic.status_code == 200:
                print("Uploading list pic...")
                s3_client.put_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=f"list/{i}.jpg",
                    Body=list_pic.content,
                    ContentType="image/jpeg",
                    ACL="public-read",
                    CacheControl="max-age=31536000"
                )
            if ("Access Denied" or "Not Found") not in str(cover_pic.content) and cover_pic.status_code == 200:
                print("Uploading cover pic...")
                s3_client.put_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=f"cover/{i}.jpg",
                    Body=cover_pic.content,
                    ContentType="image/jpeg",
                    ACL="public-read",
                    CacheControl="max-age=31536000"
                )
            if ("Access Denied" or "Not Found") not in str(
                    thumbnail_pic.content) and thumbnail_pic.status_code == 200:
                print("Uploading thumbnail pic...")
                s3_client.put_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=f"thumbnail/{i}.jpg",
                    Body=thumbnail_pic.content,
                    ContentType="image/jpeg",
                    ACL="public-read",
                    CacheControl="max-age=31536000"
                )
            self.stdout.write(self.style.SUCCESS(f"Beatmapset {i} picture has been imported to S3."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Beatmapset {i} picture import failed: {e}"))
        # sleep for 1 second to not make it too fast
        time.sleep(1)
    failed_file.close()
    self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(id_list)} beatmapset(s).'))
