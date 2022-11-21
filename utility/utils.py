from mirror.models import BeatmapSet, Beatmap
from utility.osu_database import count_beatmapset, count_beatmap


def get_beatmap_statistics() -> dict[str, int]:
    """Get statistics of beatmaps in the database"""
    return {
        'beatmapset_osu': int(count_beatmapset()),
        'beatmapset_mirror': BeatmapSet.objects.count(),
        'beatmap_osu': int(count_beatmap()),
        'beatmap_mirror': Beatmap.objects.count()
    }