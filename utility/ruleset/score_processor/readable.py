from apps.models import ScoreStore


def get_readable_osu_score(score: ScoreStore.objects) -> dict:
    """Return a readable osu! score for rendering on the website."""
    score = score.statistics
    if score['ruleset_id'] != 0:
        raise Exception("This is not an osu! ruleset score")
    statistics = score['statistics']
    maximum_statistics = score['maximum_statistics']
    try:
        mods = score['mods']
    except KeyError:
        mods = None
    try:
        great = statistics['great']
    except KeyError:
        great = 0
    try:
        ok = statistics['ok']
    except KeyError:
        ok = 0
    try:
        meh = statistics['meh']
    except KeyError:
        meh = 0
    try:
        miss = statistics['miss']
    except KeyError:
        miss = 0
    try:
        large_tick_hit = statistics['large_tick_hit']
    except KeyError:
        large_tick_hit = 0
    try:
        small_tick_hit = statistics['small_tick_hit']
    except KeyError:
        small_tick_hit = 0
    return {
        "ruleset_id": score['ruleset_id'],
        "mods": mods,
        "rank": score['rank'],
        "total_score": score['total_score'],
        "passed": score['passed'],
        "accuracy": score['accuracy'] * 100,
        "max_combo": score['max_combo'],
        "max_combo_of": maximum_statistics['great'] + maximum_statistics['large_tick_hit'],
        "great": great,
        "ok": ok,
        "meh": meh,
        "miss": miss,
        "slider_tick": large_tick_hit,
        "slider_tick_of": maximum_statistics['large_tick_hit'],
        "slider_end": small_tick_hit,
        "slider_end_of": maximum_statistics['small_tick_hit'],
    }


def get_readable_tau_score(score: ScoreStore.objects) -> dict:
    """Return a readable tau score for rendering on the website."""
    score = score.statistics
    if score['ruleset_id'] != 4:
        raise Exception("This is not a tau ruleset score")
    statistics = score['statistics']
    maximum_statistics = score['maximum_statistics']
    try:
        mods = score['mods']
    except KeyError:
        mods = None
    try:
        great = statistics['great']
    except KeyError:
        great = 0
    try:
        ok = statistics['ok']
    except KeyError:
        ok = 0
    try:
        miss = statistics['miss']
    except KeyError:
        miss = 0
    try:
        small_tick_hit = statistics['small_tick_hit']
    except KeyError:
        small_tick_hit = 0
    return {
        "ruleset_id": score['ruleset_id'],
        "mods": mods,
        "rank": score['rank'],
        "total_score": score['total_score'],
        "passed": score['passed'],
        "accuracy": score['accuracy'] * 100,
        "max_combo": score['max_combo'],
        "max_combo_of": maximum_statistics['great'],
        "great": great,
        "ok": ok,
        "miss": miss,
        "ticks": small_tick_hit,
        "ticks_of": maximum_statistics['small_tick_hit'],
    }
