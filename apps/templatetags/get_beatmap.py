from django import template

from mirror.models import Beatmap

register = template.Library()


def get_beatmap_with_beatmapset(beatmap_id: int):
    """
    Get the beatmap object by its ID. Will return None if the beatmap does not exist.
    :param beatmap_id: The ID of the beatmap.
    """
    try:
        beatmap = Beatmap.objects.get(beatmap_id=beatmap_id)
        return {
            "beatmap_id": beatmap_id,
            "beatmap": beatmap,
            "beatmapset_id": beatmap.beatmapset.beatmapset_id,
            "beatmapset": beatmap.beatmapset
        }
    except Beatmap.DoesNotExist:
        return None


register.filter('get_beatmap', get_beatmap_with_beatmapset)
