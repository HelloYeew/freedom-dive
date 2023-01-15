from django import template

register = template.Library()


def convert_json(json: dict) -> list:
    """
    Convert a JSON object to a usable dict in the template in type of list with key names and values.
    :param json: The JSON object.
    """
    new_dict = []
    for key, value in json.items():
        new_dict.append({'key': key, 'value': value})
    return new_dict


register.filter('convert_json', convert_json)
