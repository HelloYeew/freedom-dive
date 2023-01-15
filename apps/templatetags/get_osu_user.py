from apps.models import ScoreStore
from django import template

from utility.osu_database import OsuUser, get_user_by_id
from utility.ruleset.score_processor.utils import get_readable_score

register = template.Library()


def get_osu_user(user_id: int) -> OsuUser | None:
    """
    Get the detail of an osu! user by its ID from osu! database.
    :param user_id: The ID of the osu! user.
    """
    return get_user_by_id(user_id)


register.filter('get_osu_user', get_osu_user)
