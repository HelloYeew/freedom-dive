from apps.models import ScoreStore


def get_readable_score(score: ScoreStore.objects) -> dict:
    """Return a readable score for rendering on the website, will throw an error if the ruleset is not supported."""
    score = score.statistics
    statistics = score['statistics']
    maximum_statistics = score['maximum_statistics']
    if score['ruleset_id'] == 0:
        return {
            "ruleset_id": score['ruleset_id'],
            "mods": score['mods'],
            "rank": score['rank'],
            "total_score": score['total_score'],
            "passed": score['passed'],
            "accuracy": score['accuracy'] * 100,
            "max_combo": score['max_combo'],
            "max_combo_of": maximum_statistics['great'] + maximum_statistics['large_tick_hit'],
            "great": statistics['great'],
            "ok": statistics['ok'],
            "meh": statistics['meh'],
            "miss": statistics['miss'],
            "slider_tick": statistics['large_tick_hit'],
            "slider_tick_of": maximum_statistics['large_tick_hit'],
            "slider_end": statistics['small_tick_hit'],
            "slider_end_of": maximum_statistics['small_tick_hit'],
        }
    else:
        raise Exception("Ruleset not supported")
