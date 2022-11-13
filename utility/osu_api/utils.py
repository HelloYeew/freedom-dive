from datetime import datetime

from utility.osu_database.database_models import Beatmap, BeatmapSet


def create_beatmap_object_from_api(raw_api_result: dict) -> Beatmap:
    return Beatmap(
        beatmap_id=int(raw_api_result['beatmap_id']),
        beatmapset_id=int(raw_api_result['beatmapset_id']),
        user_id=int(raw_api_result['creator_id']),
        filename=f"{raw_api_result['beatmapset_id']} {raw_api_result['artist']} - {raw_api_result['title']}.osz",
        checksum=raw_api_result['file_md5'],
        version=raw_api_result['version'],
        total_length=int(raw_api_result['total_length']),
        hit_length=int(raw_api_result['hit_length']),
        count_total=int(raw_api_result['count_normal']) + int(raw_api_result['count_slider']) + int(raw_api_result['count_spinner']),
        count_normal=int(raw_api_result['count_normal']),
        count_slider=int(raw_api_result['count_slider']),
        count_spinner=int(raw_api_result['count_spinner']),
        diff_drain=float(raw_api_result['diff_drain']),
        diff_size=float(raw_api_result['diff_size']),
        diff_overall=float(raw_api_result['diff_overall']),
        diff_approach=float(raw_api_result['diff_approach']),
        play_mode=int(raw_api_result['mode']),
        approved=int(raw_api_result['approved']),
        last_update=datetime.strptime(raw_api_result['last_update'], '%Y-%m-%d %H:%M:%S'),
        difficulty_rating=float(raw_api_result['difficultyrating']),
        play_count=int(raw_api_result['playcount']),
        pass_count=int(raw_api_result['passcount']),
        bpm=float(raw_api_result['bpm'])
    )


def create_beatmapset_object_from_api(raw_api_result: dict) -> BeatmapSet:
    raw_api_result = raw_api_result[0]
    print(raw_api_result)
    print(type(raw_api_result))
    return BeatmapSet(
        beatmapset_id = int(raw_api_result['beatmapset_id']),
        user_id = int(raw_api_result['creator_id']),
        artist = raw_api_result['artist'],
        artist_unicode = raw_api_result['artist_unicode'],
        title = raw_api_result['title'],
        title_unicode = raw_api_result['title_unicode'],
        creator = raw_api_result['creator'],
        source = raw_api_result['source'],
        tags = raw_api_result['tags'],
        video = bool(int(raw_api_result['video'])),
        storyboard = bool(int(raw_api_result['storyboard'])),
        epilepsy = False,
        bpm = float(raw_api_result['bpm']),
        approved = int(raw_api_result['approved']),
        approved_date = datetime.strptime(raw_api_result['approved_date'], '%Y-%m-%d %H:%M:%S'),
        submit_date = datetime.strptime(raw_api_result['submit_date'], '%Y-%m-%d %H:%M:%S'),
        last_update = datetime.strptime(raw_api_result['last_update'], '%Y-%m-%d %H:%M:%S'),
        display_title = raw_api_result['title'],
        genre_id = int(raw_api_result['genre_id']),
        language_id = int(raw_api_result['language_id']),
        download_disabled = bool(int(raw_api_result['download_unavailable'])),
        favorite_count = int(raw_api_result['favourite_count']),
        play_count = int(raw_api_result['playcount']),
        difficulty_names = ''
    )