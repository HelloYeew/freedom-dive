from datetime import datetime

from . import get_connection
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


def insert_beatmapset_object_to_database(beatmapset: BeatmapSet):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute(f'''
        INSERT INTO osu_beatmapsets (
            beatmapset_id,
            user_id,
            artist,
            artist_unicode,
            title,
            title_unicode,
            creator,
            source,
            tags,
            video,
            storyboard,
            epilepsy,
            bpm,
            approved,
            approved_date,
            submit_date,
            last_update,
            displaytitle,
            genre_id,
            language_id,
            download_disabled,
            favourite_count,
            play_count,
            difficulty_names
        ) VALUES (
            {beatmapset.beatmapset_id},
            {beatmapset.user_id},
            {beatmapset.artist},
            {beatmapset.artist_unicode},
            {beatmapset.title},
            {beatmapset.title_unicode},
            {beatmapset.creator},
            {beatmapset.source},
            {beatmapset.tags},
            {beatmapset.video},
            {beatmapset.storyboard},
            {beatmapset.epilepsy},
            {beatmapset.bpm},
            {beatmapset.approved},
            {beatmapset.approved_date},
            {beatmapset.submit_date},
            {beatmapset.last_update},
            {beatmapset.display_title},
            {beatmapset.genre_id},
            {beatmapset.language_id},
            {beatmapset.download_disabled},
            {beatmapset.favorite_count},
            {beatmapset.play_count},
            {beatmapset.difficulty_names}
        )''')
    connection.commit()
    cursor.close()
    connection.close()


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


def insert_beatmap_object_to_database(beatmap: Beatmap):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    cursor.execute(f'''
        INSERT INTO osu_beatmaps (
            beatmap_id,
            beatmapset_id,
            user_id,
            filename,
            checksum,
            version,
            total_length,
            hit_length,
            countTotal,
            countNormal,
            countSlider
            countSpinner,
            diff_drain,
            diff_size,
            diff_overall,
            diff_approach,
            playmode
            approved,
            last_update,
            difficultyrating
            playcount,
            passcount,
            bpm
        ) VALUES (
            {beatmap.beatmap_id},
            {beatmap.beatmapset_id},
            {beatmap.user_id},
            {beatmap.filename},
            {beatmap.checksum},
            {beatmap.version},
            {beatmap.total_length},
            {beatmap.hit_length},
            {beatmap.count_total},
            {beatmap.count_normal},
            {beatmap.count_slider},
            {beatmap.count_spinner},
            {beatmap.diff_drain},
            {beatmap.diff_size},
            {beatmap.diff_overall},
            {beatmap.diff_approach},
            {beatmap.play_mode},
            {beatmap.approved},
            {beatmap.last_update},
            {beatmap.difficulty_rating},
            {beatmap.play_count},
            {beatmap.pass_count},
            {beatmap.bpm}
        )''')
    connection.commit()
    cursor.close()
    connection.close()
