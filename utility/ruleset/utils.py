ruleset_list = [
    {
        'id': 0,
        'name': 'osu!',
        'short_name': 'osu',
    },
    {
        'id': 1,
        'name': 'osu!taiko',
        'short_name': 'taiko',
    },
    {
        'id': 2,
        'name': 'osu!catch',
        'short_name': 'fruits',
    },
    {
        'id': 3,
        'name': 'osu!mania',
        'short_name': 'mania',
    },
    {
        'id': 4,
        'name': 'Tau',
        'short_name': 'tau',
    },
    {
        'id': 5,
        'name': 'Sentakki',
        'short_name': 'Sentakki',
    },
    {
        'id': 6,
        'name': 'Rush!',
        'short_name': 'rush',
    },
    {
        'id': 7,
        'name': 'Hishigata',
        'short_name': 'hishigata',
    },
    {
        'id': 8,
        'name': 'Soyokaze',
        'short_name': 'soyokaze',
    }
]


def get_ruleset_short_name(ruleset_id: int) -> str:
    """
    Get the short name of a ruleset by its ID.
    :param ruleset_id: The ID of the ruleset.
    """
    for ruleset in ruleset_list:
        if ruleset['id'] == ruleset_id:
            return ruleset['short_name']
    raise ValueError('Invalid ruleset_id: {}'.format(ruleset_id))


def get_ruleset_name(ruleset_id: int) -> str:
    """
    Get the name of a ruleset by its ID.
    :param ruleset_id: The ID of the ruleset.
    """
    for ruleset in ruleset_list:
        if ruleset['id'] == ruleset_id:
            return ruleset['name']
    raise ValueError('Invalid ruleset_id: {}'.format(ruleset_id))


def get_ruleset_id(ruleset_name: str) -> int:
    """
    Get the ID of a ruleset by its name.
    Can be either the short name or the full name.
    :param ruleset_name: The name of the ruleset.
    """
    for ruleset in ruleset_list:
        if ruleset['name'] == ruleset_name:
            return ruleset['id']
    for ruleset in ruleset_list:
        if ruleset['short_name'] == ruleset_name:
            return ruleset['id']
    raise ValueError('Invalid ruleset_name: {}'.format(ruleset_name))


def convert_ruleset_short_name_to_full_name(ruleset_short_name: str) -> str:
    """
    Convert a ruleset short name to its full name.
    :param ruleset_short_name: The short name of the ruleset.
    """
    return get_ruleset_name(get_ruleset_id(ruleset_short_name))
