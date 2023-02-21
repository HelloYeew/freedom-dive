from django.core.checks import Warning

from utility.osu_database import get_connection


def osu_database_connection_check(app_configs, **kwargs):
    """
    Check if the osu! database connection (osu!web MySQL database) is working.
    """
    try:
        get_connection()
        return []
    except Exception as e:
        return [
            Warning(
                'Cannot connect to osu! database, please check your connection to the osu! database.',
                hint='The error message is: %s' % e,
                id='OsuDatabaseConnectionCheckFailed',
            )
        ]
