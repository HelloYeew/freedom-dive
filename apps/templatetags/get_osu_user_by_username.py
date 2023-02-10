from django import template

register = template.Library()


def get_osu_user_by_username(username: str):
    """
    Get the detail of an osu! user by its username from osu! database.
    :param username: The ID of the osu! user.
    """
    from utility.osu_database import get_user_by_username
    return get_user_by_username(username)


register.filter('get_osu_user_by_username', get_osu_user_by_username)
