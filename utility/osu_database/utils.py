import mysql.connector
from decouple import config

from utility.osu_database.database_models import *
from utility.osu_database.model_utils import create_user_from_database_row, create_score_from_database_row, \
    create_beatmapset_from_database_row, create_beatmap_from_database_row


def get_connection():
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


def get_user_by_id(user_id: int) -> OsuUser:
    """Get an osu! user by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM phpbb_users WHERE user_id = %s', (user_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_user_from_database_row(row)


def get_score_by_id(score_id: int) -> Score:
    """Get a score by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM solo_scores WHERE id = %s', (score_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_score_from_database_row(row)


def get_beatmapset_by_id(beatmapset_id: int) -> BeatmapSet:
    """Get a beatmapset by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM osu_beatmapsets WHERE beatmapset_id = %s', (beatmapset_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_beatmapset_from_database_row(row)


def get_beatmap_by_id(beatmap_id: int) -> Beatmap:
    """Get a beatmap by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM osu_beatmaps WHERE beatmap_id = %s', (beatmap_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return create_beatmap_from_database_row(row)
