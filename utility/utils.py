from mirror.models import BeatmapSet, Beatmap
from utility.osu_database import count_beatmapset, count_beatmap


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
