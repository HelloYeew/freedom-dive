from datetime import datetime
import mysql.connector
from decouple import config
from models import OsuUser


def get_connection():
    """Get a connection to osu! database"""
    return mysql.connector.connect(
        host=config('MYSQL_HOST', default='localhost'),
        user=config('MYSQL_USERNAME', default='root'),
        password=config('MYSQL_PASSWORD', default=''),
        port=config('MYSQL_PORT', default='3306')
    )


def get_all_osu_user() -> list[OsuUser]:
    """Get all osu! users from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM phpbb_users')
    user_list = []
    for row in cursor:
        user_list.append(OsuUser(
            register_date=datetime.fromtimestamp(row[6]),
            username=row[7],
            username_clean=row[8],
            email=row[11],
            last_visit=datetime.fromtimestamp(row[13]),
            avatar=row[51],
            signature=row[55],
            come_from=row[58],
            country_acronym=row[76],
            twitter=row[61],
            website=row[64],
            occupation=row[65],
            interest=row[66],
            playstyle=int(row[80]),
            playmode=int(row[81]),
            is_subscriber=bool(row[71]),
            subscription_expires=datetime.fromtimestamp(row[72]) if row[72] is not None else None
        ))
    cursor.close()
    connection.close()
    return user_list


def get_osu_user(user_id: int) -> OsuUser:
    """Get an osu! user by its id from osu! database"""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute('SELECT * FROM phpbb_users WHERE user_id = %s', (user_id,))
    row = cursor.fetchone()
    user = OsuUser(
        register_date=datetime.fromtimestamp(row[6]),
        username=row[7],
        username_clean=row[8],
        email=row[11],
        last_visit=datetime.fromtimestamp(row[13]),
        avatar=row[52],
        signature=row[56],
        come_from=row[59],
        country_acronym=row[77],
        twitter=row[62],
        website=row[65],
        occupation=row[66],
        interest=row[67],
        playstyle=int(row[81]),
        playmode=int(row[82]),
        is_subscriber=bool(row[72]),
        subscription_expires=row[73]
    )
    cursor.close()
    connection.close()
    return user
