from django import template

register = template.Library()


def round_down(float_number: float) -> int:
    """
    Round a float number down to the nearest integer.
    :param float_number: The float number to round down.
    """
    return int(float_number)


register.filter('round_down', round_down)
