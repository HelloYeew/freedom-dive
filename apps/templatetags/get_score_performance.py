from apps.models import ScoreStore, PerformanceStore
from django import template

from utility.ruleset.score_processor.utils import get_readable_score

register = template.Library()


def get_score_performance(score: ScoreStore.objects) -> PerformanceStore.objects:
    """
    Get the performance or PP of a score from the database as PerformanceStore object.
    Will return None if the performance is not found.
    :param score: The score to get the performance of.
    """
    try:
        return PerformanceStore.objects.get(user_id=score.user_id, score_id=score.score_id)
    except PerformanceStore.DoesNotExist:
        return None


register.filter('get_score_performance', get_score_performance)
