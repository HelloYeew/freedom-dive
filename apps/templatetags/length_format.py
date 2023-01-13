from django import template
from time import strftime, gmtime

register = template.Library()


def length_format(length: int):
    """
    Convert second to minutes and second. Mainly use in beatmap time length.
    :param length: Length in second
    :return: Length in minutes and second format
    """
    if type(length) is not int:
        try:
            length = int(length)
        except ValueError:
            return "0:00"
    if length >= 3600:
        return strftime("%H:%M:%S", gmtime(length))
    return strftime("%M:%S", gmtime(int(length)))


register.filter('length_format', length_format)
