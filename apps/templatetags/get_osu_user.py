from django import template

from utility.osu_database import OsuUser

register = template.Library()


def get_osu_user(user_id: int) -> OsuUser | None:
    """
    Get the detail of an osu! user by its ID from osu! database.
    :param user_id: The ID of the osu! user.
    """
    from utility.osu_database import get_user_by_id
    return get_user_by_id(user_id)


register.filter('get_osu_user', get_osu_user)
