from apps.models import ScoreStore
from django import template

from utility.ruleset.score_processor.utils import get_readable_score

register = template.Library()


def get_cleaned_score(score: ScoreStore.objects) -> dict:
    """
    Get the usable result from a score object in the database.
    :param score: The score object.
    """
    return get_readable_score(score)


register.filter('get_cleaned_score', get_cleaned_score)
