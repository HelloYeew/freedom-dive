import mysql.connector
from decouple import config

from utility.osu_database.database_models import *
from utility.osu_database.model_utils import create_user_from_database_row, create_score_from_database_row, \
    create_beatmap_from_database_row, insert_beatmapset_object_to_database, \
    insert_beatmap_object_to_database, update_beatmapset_object_in_database, update_beatmap_object_in_database

BEATMAP_CREATOR_DUMMY_ID = int(config('BEATMAP_CREATOR_ID', default='10'))


def get_connection() -> mysql.connector.connection.MySQLConnection:
    """Get a connection to osu! database"""
    return mysql.connector.connect(
        host=config('MYSQL_HOST', default='localhost'),
        user=config('MYSQL_USERNAME', default='root'),
        password=config('MYSQL_PASSWORD', default=''),
        port=config('MYSQL_PORT', default='3306')
    )


def get_all_user() -> list[OsuUser]:
    """Get all osu! users from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM phpbb_users')
    user_list = []
    for row in cursor:
        user_list.append(create_user_from_database_row(row))
    cursor.close()
    connection.close()
    return user_list


def get_user_by_id(user_id: int) -> OsuUser | None:
    """Get an osu! user by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM phpbb_users WHERE user_id = %s', (user_id,))
    row = cursor.fetchone()
    if not row:
        return None
    cursor.close()
    connection.close()
    return create_user_from_database_row(row)


def get_user_by_username(username: str) -> OsuUser | None:
    """Get an osu! user by its username from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM phpbb_users WHERE username = %s', (username,))
    row = cursor.fetchone()
    if not row:
        return None
    cursor.close()
    connection.close()
    return create_user_from_database_row(row)


def get_score_by_id(score_id: int) -> Score | None:
    """Get a score by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM solo_scores WHERE id = %s', (score_id,))
    row = cursor.fetchone()
    if not row:
        return None
    cursor.close()
    connection.close()
    return create_score_from_database_row(row)


def get_beatmapset_by_id(beatmapset_id: int) -> BeatmapSet | None:
    """Get a beatmapset by its id from osu! database"""
    from utility.osu_database.model_utils import create_beatmapset_from_database_row
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute(f'SELECT * FROM osu_beatmapsets WHERE beatmapset_id = {beatmapset_id};')
    row = cursor.fetchone()
    if not row:
        return None
    cursor.close()
    connection.close()
    return create_beatmapset_from_database_row(row)


def get_beatmap_by_id(beatmap_id: int) -> Beatmap | None:
    """Get a beatmap by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM osu_beatmaps WHERE beatmap_id = %s', (beatmap_id,))
    row = cursor.fetchone()
    if not row:
        return None
    cursor.close()
    connection.close()
    return create_beatmap_from_database_row(row)


def get_beatmap_by_beatmapset(beatmapset_id: int) -> list[Beatmap]:
    """Get all beatmaps in a beatmapset from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM osu_beatmaps WHERE beatmapset_id = %s', (beatmapset_id,))
    beatmap_list = []
    for row in cursor:
        beatmap_list.append(create_beatmap_from_database_row(row))
    cursor.close()
    connection.close()
    return beatmap_list


def import_beatmapset_from_api(beatmapset_id: int):
    """Import a beatmapset and beatmap in beatmapset to osu! database"""
    from utility.osu_api import get_beatmapset_object_from_api, get_beatmap_object_list_from_api
    beatmapset = get_beatmapset_object_from_api(beatmapset_id)
    if beatmapset is None:
        return
    beatmapset.user_id = BEATMAP_CREATOR_DUMMY_ID
    insert_beatmapset_object_to_database(beatmapset)
    for beatmap in get_beatmap_object_list_from_api(beatmapset_id):
        beatmap.user_id = BEATMAP_CREATOR_DUMMY_ID
        insert_beatmap_object_to_database(beatmap)


def update_beatmapset_from_api(beatmapset_id: int):
    """Update a beatmapset and beatmap in beatmapset to osu! database"""
    from utility.osu_api import get_beatmapset_object_from_api, get_beatmap_object_list_from_api
    beatmapset = get_beatmapset_object_from_api(beatmapset_id)
    if beatmapset is None:
        return
    beatmapset.user_id = BEATMAP_CREATOR_DUMMY_ID
    update_beatmapset_object_in_database(beatmapset)
    for beatmap in get_beatmap_object_list_from_api(beatmapset_id):
        beatmap.user_id = BEATMAP_CREATOR_DUMMY_ID
        update_beatmap_object_in_database(beatmap)


def count_beatmapset() -> int:
    """Count the number of beatmapset in osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT COUNT(*) FROM osu_beatmapsets;')
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count


def count_beatmap() -> int:
    """Count the number of beatmap in osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT COUNT(*) FROM osu_beatmaps;')
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count
