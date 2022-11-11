import json
import requests
from decouple import config

OSU_API_KEY = config('OSU_API_KEY', default='')
OSU_API_URL = 'https://osu.ppy.sh/api'


def get_beatmap_info(beatmap_id: int) -> dict:
    """Get beatmap info from osu! api"""
    response = requests.get(f'{OSU_API_URL}/get_beatmaps', params={
        'k': OSU_API_KEY,
        'b': beatmap_id
    })
    return response.json()


def get_beatmapset_info(beatmapset_id: int) -> dict:
    """Get beatmapset info from osu! api"""
    response = requests.get(f'{OSU_API_URL}/get_beatmaps', params={
        'k': OSU_API_KEY,
        's': beatmapset_id
    })
    return response.json()


def get_user_info(user_id: int) -> dict:
    """Get user info from osu! api"""
    response = requests.get(f'{OSU_API_URL}/get_user', params={
        'k': OSU_API_KEY,
        'u': user_id
    })
    return response.json()

# print with indented
print(json.dumps(get_user_info(2), indent=4))