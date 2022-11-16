import time
import traceback

import requests
from decouple import config
from django.core.management import BaseCommand
from django.utils import timezone
from mysql.connector import InterfaceError, IntegrityError

from mirror import models
from mirror.models import BeatmapSet
from utility.osu_database import get_beatmapset_by_id, import_beatmapset_from_api, update_beatmapset_from_api, \
    get_beatmap_by_beatmapset, Beatmap
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
        s3_client = get_s3_client()
        # create text file for store failed beatmapset id
        failed_file = open("failed.txt", "w")
        # add ---------- to separate each import
        failed_file.write("----------\n")
        # loop through beatmapset id
        for i in range(start, end + 1):
            try:
                # find beatmapset by id in osu! database
                beatmapset = get_beatmapset_by_id(i)
                if beatmapset:
                    self.stdout.write(self.style.SUCCESS('Beatmapset "%s" already exists in database, updating...' % beatmapset.title))
                    update_beatmapset_from_api(i)
                    import_beatmapset_to_mirror(beatmapset)
                    beatmapset = get_beatmap_by_beatmapset(i)
                    for beatmap in beatmapset:
                        import_beatmap_to_mirror(beatmap)
                    print(f"Beatmapset {i} has been updated.")
                else:
                    self.stdout.write(self.style.SUCCESS('Beatmapset with id "%s" not found in database, importing...' % i))
                    import_beatmapset_from_api(i)
                    self.stdout.write(self.style.SUCCESS(f"Beatmapset {i} has been imported, importing to mirror database..."))
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
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {start} to {end} beatmapsets'))


def import_beatmapset_to_mirror(beatmapset:BeatmapSet):
    beatmapset_mirror = models.BeatmapSet.objects.filter(beatmapset_id=beatmapset.beatmapset_id).exists()
    if not beatmapset_mirror:
        models.BeatmapSet.objects.create(
            beatmapset_id=beatmapset.beatmapset_id,
            user_id=beatmapset.user_id,
            artist=beatmapset.artist,
            artist_unicode=beatmapset.artist_unicode,
            title=beatmapset.title,
            title_unicode=beatmapset.title_unicode,
            creator=beatmapset.creator,
            source=beatmapset.source,
            tags=beatmapset.tags,
            video=beatmapset.video,
            storyboard=beatmapset.storyboard,
            epilepsy=beatmapset.epilepsy,
            bpm=beatmapset.bpm,
            approved=beatmapset.approved,
            approved_date=timezone.make_aware(beatmapset.approved_date) if beatmapset.approved_date else None,
            submit_date=timezone.make_aware(beatmapset.submit_date) if beatmapset.submit_date else None,
            last_update=timezone.make_aware(beatmapset.last_update) if beatmapset.last_update else None,
            display_title=beatmapset.display_title,
            genre_id=beatmapset.genre_id,
            language_id=beatmapset.language_id,
            download_disabled=beatmapset.download_disabled,
            favorite_count=beatmapset.favorite_count,
            play_count=beatmapset.play_count,
            difficulty_names=beatmapset.difficulty_names
        )
    else:
        beatmapset_mirror = models.BeatmapSet.objects.get(beatmapset_id=beatmapset.beatmapset_id)
        beatmapset_mirror.user_id = beatmapset.user_id
        beatmapset_mirror.artist = beatmapset.artist
        beatmapset_mirror.artist_unicode = beatmapset.artist_unicode
        beatmapset_mirror.title = beatmapset.title
        beatmapset_mirror.title_unicode = beatmapset.title_unicode
        beatmapset_mirror.creator = beatmapset.creator
        beatmapset_mirror.source = beatmapset.source
        beatmapset_mirror.tags = beatmapset.tags
        beatmapset_mirror.video = beatmapset.video
        beatmapset_mirror.storyboard = beatmapset.storyboard
        beatmapset_mirror.epilepsy = beatmapset.epilepsy
        beatmapset_mirror.bpm = beatmapset.bpm
        beatmapset_mirror.approved = beatmapset.approved
        beatmapset_mirror.approved_date = timezone.make_aware(beatmapset.approved_date) if beatmapset.approved_date else None
        beatmapset_mirror.submit_date = timezone.make_aware(beatmapset.submit_date) if beatmapset.submit_date else None
        beatmapset_mirror.last_update = timezone.make_aware(beatmapset.last_update) if beatmapset.last_update else None
        beatmapset_mirror.display_title = beatmapset.display_title
        beatmapset_mirror.genre_id = beatmapset.genre_id
        beatmapset_mirror.language_id = beatmapset.language_id
        beatmapset_mirror.download_disabled = beatmapset.download_disabled
        beatmapset_mirror.favorite_count = beatmapset.favorite_count
        beatmapset_mirror.play_count = beatmapset.play_count
        beatmapset_mirror.difficulty_names = beatmapset.difficulty_names
        beatmapset_mirror.save()


def import_beatmap_to_mirror(beatmap:Beatmap):
    beatmap_mirror = models.Beatmap.objects.filter(beatmap_id=beatmap.beatmap_id).exists()
    if not beatmap_mirror:
        beatmapset_mirror = models.BeatmapSet.objects.get(beatmapset_id=beatmap.beatmapset_id)
        models.Beatmap.objects.create(
            beatmap_id=beatmap.beatmap_id,
            beatmapset=beatmapset_mirror,
            user_id=BEATMAP_CREATOR_DUMMY_ID,
            filename=beatmap.filename,
            checksum=beatmap.checksum,
            version=beatmap.version,
            total_length=beatmap.total_length,
            hit_length=beatmap.hit_length,
            count_total=beatmap.count_total,
            count_normal=beatmap.count_normal,
            count_slider=beatmap.count_slider,
            count_spinner=beatmap.count_spinner,
            diff_drain=beatmap.diff_drain,
            diff_size=beatmap.diff_size,
            diff_overall=beatmap.diff_overall,
            diff_approach=beatmap.diff_approach,
            play_mode=beatmap.play_mode,
            approved=beatmap.approved,
            last_update=timezone.make_aware(beatmap.last_update) if beatmap.last_update else None,
            difficulty_rating=beatmap.difficulty_rating,
            play_count=beatmap.play_count,
            pass_count=beatmap.pass_count,
            bpm=beatmap.bpm,
        )
    else:
        beatmap_mirror = models.Beatmap.objects.get(beatmap_id=beatmap.beatmap_id)
        beatmap_mirror.user_id = BEATMAP_CREATOR_DUMMY_ID
        beatmap_mirror.filename = beatmap.filename
        beatmap_mirror.checksum = beatmap.checksum
        beatmap_mirror.version = beatmap.version
        beatmap_mirror.total_length = beatmap.total_length
        beatmap_mirror.hit_length = beatmap.hit_length
        beatmap_mirror.count_total = beatmap.count_total
        beatmap_mirror.count_normal = beatmap.count_normal
        beatmap_mirror.count_slider = beatmap.count_slider
        beatmap_mirror.count_spinner = beatmap.count_spinner
        beatmap_mirror.diff_drain = beatmap.diff_drain
        beatmap_mirror.diff_size = beatmap.diff_size
        beatmap_mirror.diff_overall = beatmap.diff_overall
        beatmap_mirror.diff_approach = beatmap.diff_approach
        beatmap_mirror.play_mode = beatmap.play_mode
        beatmap_mirror.approved = beatmap.approved
        beatmap_mirror.last_update = timezone.make_aware(beatmap.last_update) if beatmap.last_update else None
        beatmap_mirror.difficulty_rating = beatmap.difficulty_rating
        beatmap_mirror.play_count = beatmap.play_count
        beatmap_mirror.pass_count = beatmap.pass_count
        beatmap_mirror.bpm = beatmap.bpm
        beatmap_mirror.save()