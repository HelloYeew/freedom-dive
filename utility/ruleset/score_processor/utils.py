from apps.models import ScoreStore
from utility.ruleset.score_processor.readable import get_readable_osu_score, get_readable_tau_score


def get_readable_score(score: ScoreStore.objects) -> dict:
    """Return a readable score for rendering on the website, will throw an error if the ruleset is not supported."""
    score_statistics = score.statistics
    if score_statistics['ruleset_id'] == 0:
        return get_readable_osu_score(score)
    elif score_statistics['ruleset_id'] == 4:
        return get_readable_tau_score(score)
    else:
        raise Exception("Ruleset not supported")
