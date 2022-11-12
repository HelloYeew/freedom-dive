from datetime import datetime

from utility.osu_database.models import OsuUser, Score


def create_user_from_database_row(db_row: tuple) -> OsuUser:
    """Create an OsuUser from a database row"""
    return OsuUser(
        register_date=datetime.fromtimestamp(db_row[6]),
        username=db_row[7],
        username_clean=db_row[8],
        email=db_row[11],
        last_visit=datetime.fromtimestamp(db_row[13]),
        avatar=db_row[52],
        signature=db_row[56],
        come_from=db_row[59],
        country_acronym=db_row[77],
        twitter=db_row[62],
        website=db_row[65],
        occupation=db_row[66],
        interest=db_row[67],
        playstyle=int(db_row[81]),
        playmode=int(db_row[82]),
        is_subscriber=bool(db_row[72]),
        subscription_expires=db_row[73]
    )


def create_score_from_database_row(db_row: tuple) -> Score:
    """Create a Score from a database row"""
    return Score(
        database_id=db_row[0],
        user_id=db_row[1],
        beatmap_id=db_row[2],
        ruleset_id=db_row[3],
        data=db_row[4],
        has_replay=bool(db_row[5]),
        preserve=bool(db_row[6]),
        created_at=datetime.fromtimestamp(db_row[7]),
        updated_at=datetime.fromtimestamp(db_row[8])
    )
