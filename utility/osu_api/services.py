import json
import requests
from decouple import config

from utility.osu_api.utils import create_beatmap_object_from_api
from utility.osu_database.database_models import Beatmap

OSU_API_KEY = config('OSU_API_KEY', default='')
OSU_API_URL = 'https://osu.ppy.sh/api'


def get_raw_beatmap_info(beatmap_id: int) -> dict:
    """Get beatmap info from osu! api"""
    response = requests.get(f'{OSU_API_URL}/get_beatmaps', params={
        'k': OSU_API_KEY,
        'b': beatmap_id
    })
    return response.json()


def get_raw_beatmapset_info(beatmapset_id: int) -> dict:
    """Get beatmapset info from osu! api"""
    response = requests.get(f'{OSU_API_URL}/get_beatmaps', params={
        'k': OSU_API_KEY,
        's': beatmapset_id
    })
    return response.json()


def get_raw_user_info(user_id: int) -> dict:
    """Get user info from osu! api"""
    response = requests.get(f'{OSU_API_URL}/get_user', params={
        'k': OSU_API_KEY,
        'u': user_id
    })
    return response.json()


def get_beatmap_object_list_from_api(beatmapset_id: int) -> list[Beatmap]:
    """Get a list of Beatmap objects from osu! api"""
    raw_api_result = get_raw_beatmapset_info(beatmapset_id)
    return [create_beatmap_object_from_api(beatmap) for beatmap in raw_api_result]
