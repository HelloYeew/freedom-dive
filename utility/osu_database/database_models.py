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

    def __init__(self, database_id: int, user_id: int, beatmap_id: int, ruleset_id: int, data: dict, has_replay: bool,
                 preserve: bool, created_at: datetime, updated_at: datetime):
        """
        Initialize a Score object

        :param database_id: score id (id)
        :param user_id: user id (user_id)
        :param beatmap_id: beatmap id (beatmap_id)
        :param ruleset_id: ruleset id (ruleset_id)
        :param data: score data (data)
        :param has_replay: has replay (has_replay)
        :param preserve: preserve (preserve)
        :param created_at: created at (created_at)
        :param updated_at: updated at (updated_at)
        """
        self.database_id = database_id
        self.user_id = user_id
        self.beatmap_id = beatmap_id
        self.ruleset_id = ruleset_id
        self.data = data
        self.has_replay = has_replay
        self.preserve = preserve
        self.created_at = created_at
        self.updated_at = updated_at


class BeatmapSet:
    """A model that represents a beatmap set (osu_beatmapsets table in osu! database)"""

    def __init__(self, beatmapset_id: int, user_id: int, artist: str, artist_unicode: str, title: str,
                 title_unicode: str, creator: str, source: str, tags: str, video: bool, storyboard: bool,
                 epilepsy: bool, bpm: float, approved: int, approved_date: datetime, submit_date: datetime,
                 last_update: datetime, display_title: str, genre_id: int, language_id: int,
                 download_disabled: bool, favorite_count: int, play_count: int, difficulty_names: str):
        """
        Initialize a BeatmapSet object

        :param beatmapset_id: beatmap set id (beatmapset_id)
        :param user_id: user id (user_id)
        :param artist: artist (artist)
        :param artist_unicode: artist unicode (artist_unicode)
        :param title: title (title)
        :param title_unicode: title unicode (title_unicode)
        :param creator: creator (creator)
        :param source: source (source)
        :param tags: tags (tags)
        :param video: video (video)
        :param storyboard: storyboard (storyboard)
        :param epilepsy: epilepsy (epilepsy)
        :param bpm: bpm (bpm)
        :param approved: approved status (approved)
        :param approved_date: approved date (approved_date)
        :param submit_date: submit date (submit_date)
        :param last_update: last update (last_update)
        :param display_title: display title (displaytitle)
        :param genre_id: genre id (genre_id)
        :param language_id: language id (language_id)
        :param download_disabled: download disabled (download_disabled)
        :param favorite_count: favorite count (favourite_count)
        :param play_count: play count (playcount)
        :param difficulty_names: difficulty names (difficulty_names)
        """
        self.beatmapset_id = beatmapset_id
        self.user_id = user_id
        self.artist = artist
        self.artist_unicode = artist_unicode
        self.title = title
        self.title_unicode = title_unicode
        self.creator = creator
        self.source = source
        self.tags = tags
        self.video = video
        self.storyboard = storyboard
        self.epilepsy = epilepsy
        self.bpm = bpm
        self.approved = approved
        self.approved_date = approved_date
        self.submit_date = submit_date
        self.last_update = last_update
        self.display_title = display_title
        self.genre_id = genre_id
        self.language_id = language_id
        self.download_disabled = download_disabled
        self.favorite_count = favorite_count
        self.play_count = play_count
        self.difficulty_names = difficulty_names


class Beatmap:
    """A model that represents a beatmap (osu_beatmaps table in osu! database)"""

    def __init__(self, beatmap_id: int, beatmapset_id: int, user_id: int, filename: str, checksum: str, version: str,
                 total_length: int, hit_length: int, count_total: int, count_normal: int, count_slider: int,
                 count_spinner: int, diff_drain: float, diff_size: float, diff_overall: float, diff_approach: float,
                 play_mode: int, approved: int, last_update: datetime, difficulty_rating: float, play_count: int,
                 pass_count: int, bpm: float):
        """
        Initialize a Beatmap object

        :param beatmap_id: beatmap id (beatmap_id)
        :param beatmapset_id: beatmap set id (beatmapset_id)
        :param user_id: user id (user_id)
        :param filename: filename (filename)
        :param checksum: checksum (checksum)
        :param version: version (version)
        :param total_length: seconds from first note to last note including breaks (total_length)
        :param hit_length: hit length (hit_length)
        :param count_total: count total (countTotal)
        :param count_normal: count normal (countNormal)
        :param count_slider: count slider (countSlider)
        :param count_spinner: count spinner (countSpinner)
        :param diff_drain: diff drain (diff_drain)
        :param diff_size: diff size (diff_size)
        :param diff_overall: diff overall (diff_overall)
        :param diff_approach: diff approach (diff_approach)
        :param play_mode: playmode (playmode)
        :param approved: approved status (approved)
        :param last_update: last update (last_update)
        :param difficulty_rating: difficulty rating (difficultyrating)
        :param play_count: play count (playcount)
        :param pass_count: pass count (passcount)
        :param bpm: bpm (bpm)
        """
        self.beatmap_id = beatmap_id
        self.beatmapset_id = beatmapset_id
        self.user_id = user_id
        self.filename = filename
        self.checksum = checksum
        self.version = version
        self.total_length = total_length
        self.hit_length = hit_length
        self.count_total = count_total
        self.count_normal = count_normal
        self.count_slider = count_slider
        self.count_spinner = count_spinner
        self.diff_drain = diff_drain
        self.diff_size = diff_size
        self.diff_overall = diff_overall
        self.diff_approach = diff_approach
        self.play_mode = play_mode
        self.approved = approved
        self.last_update = last_update
        self.difficulty_rating = difficulty_rating
        self.play_count = play_count
        self.pass_count = pass_count
        self.bpm = bpm

    def beatmapset(self) -> BeatmapSet:
        """
        Get the beatmap set of this beatmap

        :return: the beatmap set of this beatmap
        """
        return get_beatmapset_by_id(self.beatmapset_id)
