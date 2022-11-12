from datetime import datetime

from .database_models import *


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


def create_beatmapset_from_database_row(db_row: tuple) -> BeatmapSet:
    """Create a Beatmapset from a database row"""
    return BeatmapSet(
        beatmapset_id=db_row[0],
        user_id=db_row[1],
        artist=db_row[3],
        artist_unicode=db_row[4],
        title=db_row[5],
        title_unicode=db_row[6],
        creator=db_row[7],
        source=db_row[8],
        tags=db_row[9],
        video=bool(db_row[10]),
        storyboard=bool(db_row[11]),
        epilepsy=bool(db_row[12]),
        bpm=db_row[13],
        approved=db_row[15],
        approved_date=db_row[17],
        submit_date=db_row[18],
        last_update=db_row[19],
        display_title=db_row[24],
        genre_id=db_row[25],
        language_id=db_row[26],
        download_disabled=bool(db_row[32]),
        favorite_count=db_row[36],
        play_count=db_row[37],
        difficulty_names=db_row[38]
    )


def create_beatmap_from_database_row(db_row: tuple) -> Beatmap:
    """Create a Beatmap from a database row"""
    return Beatmap(
        beatmap_id=db_row[0],
        beatmapset_id=db_row[1],
        user_id=db_row[2],
        filename=db_row[3],
        checksum=db_row[4],
        version=db_row[5],
        total_length=db_row[6],
        hit_length=db_row[7],
        count_total=db_row[8],
        count_normal=db_row[9],
        count_slider=db_row[10],
        count_spinner=db_row[11],
        diff_drain=db_row[12],
        diff_size=db_row[13],
        diff_overall=db_row[14],
        diff_approach=db_row[15],
        play_mode=db_row[16],
        approved=db_row[17],
        last_update=db_row[18],
        difficulty_rating=db_row[19],
        play_count=db_row[20],
        pass_count=db_row[21],
        bpm=db_row[26]
    )

