import mysql.connector
from decouple import config

from models import OsuUser
from utility.osu_database.model_utils import create_user_from_database_row


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


# TODO: Solo score import