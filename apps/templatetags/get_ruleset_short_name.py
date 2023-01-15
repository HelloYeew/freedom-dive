from django import template

from utility.ruleset.utils import get_ruleset_short_name

register = template.Library()


def get_ruleset_name(ruleset_id: int):
    """
    Get the short name of a ruleset by its ID.
    :param ruleset_id: The ID of the ruleset.
    """
    return get_ruleset_short_name(ruleset_id)


register.filter('get_ruleset_short_name', get_ruleset_name)
