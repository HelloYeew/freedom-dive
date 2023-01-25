import json

import requests
import urllib.parse

import sentry_sdk
from decouple import config

OSU_API_CLIENT_ID = config('OSU_API_CLIENT_ID', default='')
OSU_API_CLIENT_SECRET = config('OSU_API_CLIENT_SECRET', default='')


def generate_authorize_url(client_id: int = OSU_API_CLIENT_ID, redirect_uri: str = None, response_type: str = 'code',
                           scope: str = 'public'):
    return f'https://osu.ppy.sh/oauth/authorize?client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&response_type={response_type}&scope={scope}'


def get_access_token(code: str, client_id: int = OSU_API_CLIENT_ID, client_secret: str = OSU_API_CLIENT_SECRET, redirect_uri: str = None):
    request_payload = json.dumps({
        'client_id': int(client_id),
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", 'https://osu.ppy.sh/oauth/token', headers=headers, data=request_payload)
    try:
        # return converted response.text to json
        return json.loads(response.text)
    except Exception as e:
        sentry_sdk.set_context("payload", request_payload)
        sentry_sdk.capture_exception(e)
        return None
