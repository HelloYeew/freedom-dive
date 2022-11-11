from datetime import datetime


class OsuUser:
    """A model that represents an osu! user (phpbb_users table in osu! database)"""

    def __init__(self, register_date: datetime, username: str, username_clean: str, email: str, last_visit: datetime,
                 avatar: str, signature: str, come_from: str, country_acronym: str, twitter: str, website: str,
                 occupation: str, interest: str, playstyle: int, playmode: int, is_subscriber: bool,
                 subscription_expires: datetime.date):
        """
        Initialize an OsuUser object

        :param register_date: date of registration (user_regdate)
        :param username: username (username)
        :param username_clean: username without special characters (username_clean)
        :param email: email (user_email)
        :param last_visit: last visit (user_lastvisit)
        :param avatar: avatar file name (user_avatar)
        :param signature: signature (user_sig)
        :param come_from: come from (user_from)
        :param country_acronym: country acronym (country_acronym)
        :param twitter: twitter (user_twitter)
        :param website: website (user_website)
        :param occupation: occupation (user_occ)
        :param interest: interest (user_interests)
        :param playstyle: playstyle (osu_playstyle)
        :param playmode: playmode (osu_playmode)
        :param is_subscriber: is subscriber (osu_subscriber)
        :param subscription_expires: subscription expires (osu_subscriptionexpiry)
        """
        self.register_date = register_date
        self.username = username
        self.username_clean = username_clean
        self.email = email
        self.last_visit = last_visit
        self.avatar = avatar
        self.signature = signature
        self.come_from = come_from
        self.country_acronym = country_acronym
        self.twitter = twitter
        self.website = website
        self.occupation = occupation
        self.interest = interest
        self.playstyle = playstyle
        self.playmode = playmode
        self.is_subscriber = is_subscriber
        self.subscription_expires = subscription_expires


class Score:
    """A model that represents a score (solo_scores table in osu! database)"""
    def __init__(self, user_id: int, beatmap_id: int, ruleset_id: int, data: dict, has_replay: bool, preserve: bool,
                 created_at: datetime, updated_at: datetime):
        self.user_id = user_id
        self.beatmap_id = beatmap_id
        self.ruleset_id = ruleset_id
        self.data = data
        self.has_replay = has_replay
        self.preserve = preserve
        self.created_at = created_at
        self.updated_at = updated_at
