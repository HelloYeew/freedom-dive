def get_ruleset_short_name(ruleset_id: int) -> str:
    """
    Get the short name of a ruleset by its ID.
    :param ruleset_id: The ID of the ruleset.
    """
    if ruleset_id == 0:
        return 'osu'
    elif ruleset_id == 1:
        return 'taiko'
    elif ruleset_id == 2:
        return 'fruits'
    elif ruleset_id == 3:
        return 'mania'
    elif ruleset_id == 4:
        return 'tau'
    elif ruleset_id == 5:
        return 'Sentakki'
    elif ruleset_id == 6:
        return 'rush'
    elif ruleset_id == 7:
        return 'hishigata'
    elif ruleset_id == 8:
        return "soyokaze"
    else:
        raise ValueError('Invalid ruleset_id: {}'.format(ruleset_id))


def get_ruleset_name(ruleset_id: int) -> str:
    """
    Get the name of a ruleset by its ID.
    :param ruleset_id: The ID of the ruleset.
    """
    if ruleset_id == 0:
        return 'osu!'
    elif ruleset_id == 1:
        return 'osu!taiko'
    elif ruleset_id == 2:
        return 'osu!catch'
    elif ruleset_id == 3:
        return 'osu!mania'
    elif ruleset_id == 4:
        return 'Tau'
    elif ruleset_id == 5:
        return 'Sentakki'
    elif ruleset_id == 6:
        return 'Rush!'
    elif ruleset_id == 7:
        return 'Hishigata'
    elif ruleset_id == 8:
        return 'Soyokaze'
    else:
        raise ValueError('Invalid ruleset_id (ID: {})'.format(ruleset_id))
