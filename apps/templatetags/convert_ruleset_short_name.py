from django import template

from utility.ruleset.utils import convert_ruleset_short_name_to_full_name

register = template.Library()


def convert_ruleset_short_name(ruleset_short_name: str) -> str:
    """
    Convert a ruleset short name to its full name.
    :param ruleset_short_name: The short name of the ruleset.
    """
    return convert_ruleset_short_name_to_full_name(ruleset_short_name)


register.filter('convert_ruleset_short_name', convert_ruleset_short_name)
