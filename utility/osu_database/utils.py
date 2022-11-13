import mysql.connector
from decouple import config

from utility.osu_api import get_beatmapset_object_from_api, get_beatmap_object_list_from_api
from utility.osu_database.database_models import *
from utility.osu_database.model_utils import create_user_from_database_row, create_score_from_database_row, \
    create_beatmapset_from_database_row, create_beatmap_from_database_row, insert_beatmapset_object_to_database, \
    insert_beatmap_object_to_database


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
    if cursor.rowcount == 0:
        return None
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_user_from_database_row(row)


def get_score_by_id(score_id: int) -> Score | None:
    """Get a score by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM solo_scores WHERE id = %s', (score_id,))
    if cursor.rowcount == 0:
        return None
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_score_from_database_row(row)


def get_beatmapset_by_id(beatmapset_id: int) -> BeatmapSet | None:
    """Get a beatmapset by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM osu_beatmapsets WHERE beatmapset_id = %s', (beatmapset_id,))
    if cursor.rowcount == 0:
        return None
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_beatmapset_from_database_row(row)


def get_beatmap_by_id(beatmap_id: int) -> Beatmap | None:
    """Get a beatmap by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM osu_beatmaps WHERE beatmap_id = %s', (beatmap_id,))
    if cursor.rowcount == 0:
        return None
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_beatmap_from_database_row(row)


def import_beatmapset_from_api(beatmapset_id: int):
    """Import a beatmapset and beatmap in beatmapset to osu! database"""
    beatmapset = get_beatmapset_object_from_api(beatmapset_id)
    insert_beatmapset_object_to_database(beatmapset)
    for beatmap in get_beatmap_object_list_from_api(beatmapset_id):
        insert_beatmap_object_to_database(beatmap)