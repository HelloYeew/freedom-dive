from datetime import datetime

from utility.osu_database.database_models import Beatmap


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