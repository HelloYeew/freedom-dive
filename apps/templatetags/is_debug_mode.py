from django import template
from django.conf import settings

register = template.Library()


def is_debug_mode() -> bool:
    """
    Return true if Django's environment is debug mode.
    """
    return settings.DEBUG


register.filter('is_debug_mode', is_debug_mode)
