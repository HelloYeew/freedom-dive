from django import template

from mirror.models import ScoreStore
from utility.ruleset.score_processor.utils import get_readable_score

register = template.Library()


def get_readable_score_from_processor(score_id: int):
    """
    Get the readable score from the score processor.
    :param score_id: The ID of the score.
    """
    try:
        return get_readable_score(ScoreStore.objects.get(id=score_id))
    except ScoreStore.DoesNotExist:
        return None


register.filter('get_readable_score', get_readable_score_from_processor)
