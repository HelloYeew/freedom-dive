from mirror.models import Country
from django import template

register = template.Library()


def get_osu_country(acronym: str) -> Country.objects:
    """
    Get country by its acronym from mirror database.
    Will return None if the country does not exist.
    :param acronym: The acronym of the country.
    """
    try:
        return Country.objects.get(acronym=acronym)
    except Country.DoesNotExist:
        return None


register.filter('get_osu_country', get_osu_country)
