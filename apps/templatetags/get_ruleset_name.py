from django import template

from utility.ruleset.utils import get_ruleset_name

register = template.Library()


def get_ruleset_full_name(ruleset_id: int):
    """
    Get the full name of a ruleset by its ID.
    :param ruleset_id: The ID of the ruleset.
    """
    return get_ruleset_name(ruleset_id)


register.filter('get_ruleset_name', get_ruleset_full_name)
