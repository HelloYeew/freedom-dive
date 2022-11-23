import requests
from decouple import config

from mirror.models import BeatmapSet, Beatmap
from utility.osu_database import count_beatmapset, count_beatmap
from utility.s3.utils import get_s3_client

S3_BUCKET_NAME = config('S3_BUCKET_NAME', default='')


def get_osu_beatmap_statistics() -> dict[str, int]:
    """Get statistics of beatmaps in the osu! database."""
    return {
        'beatmapset': int(count_beatmapset()),
        'beatmap': int(count_beatmap()),
    }


def get_mirror_beatmap_statistics() -> dict[str, int]:
    """Get statistics of beatmaps in the mirror database."""
    return {
        'beatmapset': BeatmapSet.objects.count(),
        'beatmap': Beatmap.objects.count()
    }


def download_beatmap_pic_to_s3(beatmap_id: int):
    """Import beatmap picture from osu! website to S3."""
    s3_client = get_s3_client()
    card_pic = requests.get(f"https://assets.ppy.sh/beatmaps/{beatmap_id}/covers/card.jpg")
    list_pic = requests.get(f"https://assets.ppy.sh/beatmaps/{beatmap_id}/covers/list.jpg")
    cover_pic = requests.get(f"https://assets.ppy.sh/beatmaps/{beatmap_id}/covers/cover.jpg")
    thumbnail_pic = requests.get(f"https://b.ppy.sh/thumb/{beatmap_id}l.jpg")
    if ("Access Denied" or "Not Found") not in str(card_pic.content) and card_pic.status_code == 200:
        print("Uploading card pic...")
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"card/{beatmap_id}.jpg",
            Body=card_pic.content,
            ContentType="image/jpeg",
            ACL="public-read",
            CacheControl="max-age=31536000"
        )
    if ("Access Denied" or "Not Found") not in str(list_pic.content) and list_pic.status_code == 200:
        print("Uploading list pic...")
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"list/{beatmap_id}.jpg",
            Body=list_pic.content,
            ContentType="image/jpeg",
            ACL="public-read",
            CacheControl="max-age=31536000"
        )
    if ("Access Denied" or "Not Found") not in str(cover_pic.content) and cover_pic.status_code == 200:
        print("Uploading cover pic...")
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"cover/{beatmap_id}.jpg",
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
            Key=f"thumbnail/{beatmap_id}.jpg",
            Body=thumbnail_pic.content,
            ContentType="image/jpeg",
            ACL="public-read",
            CacheControl="max-age=31536000"
        )
