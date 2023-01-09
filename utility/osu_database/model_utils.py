from .database_models import *


def create_user_from_database_row(db_row: tuple) -> OsuUser:
    """Create an OsuUser from a database row"""
    return OsuUser(
        user_id=db_row[0],
        register_date=datetime.fromtimestamp(db_row[6]),
        username=db_row[7],
        username_clean=db_row[8],
        email=db_row[11],
        last_visit=datetime.fromtimestamp(db_row[13]),
        avatar=db_row[52],
        signature=db_row[56].decode('utf-8') if type(db_row[56]) is bytes else db_row[56],
        come_from=db_row[59].decode('utf-8') if type(db_row[59]) is bytes else db_row[59],
        country_acronym=db_row[77],
        twitter=db_row[62],
        website=db_row[65],
        occupation=db_row[66].decode('utf-8') if type(db_row[66]) is bytes else db_row[66],
        interest=db_row[67].decode('utf-8') if type(db_row[67]) is bytes else db_row[67],
        playstyle=int(db_row[81]),
        playmode=int(db_row[82]),
        is_subscriber=bool(db_row[72]),
        subscription_expires=db_row[73]
    )


def insert_user_to_database(user: OsuUser):
    """Insert an OsuUser to the database"""
    # Import the database connection locally to avoid circular imports
    from utility.osu_database.utils import get_connection
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    command = f'''
        INSERT INTO phpbb_users (
            user_regdate,
            username,
            username_clean,
            user_email,
            user_lastvisit,
            user_avatar,
            user_sig,
            user_from,
            country_acronym,
            user_twitter,
            user_website,
            user_occ,
            user_interests,
            osu_playstyle,
            osu_playmode,
            osu_subscriber,
            osu_subscriptionexpiry,
            user_permissions
        ) VALUES (
            {int(user.register_date.timestamp())},
            {"'" + user.username + "'"},
            {"'" + user.username_clean + "'"},
            {"'" + user.email + "'"},
            {int(user.last_visit.timestamp())},
            {"'" + user.avatar + "'"},
            {"'" + user.signature + "'"},
            {"'" + user.come_from + "'"},
            {"'" + user.country_acronym + "'"},
            {"'" + user.twitter + "'"},
            {"'" + user.website + "'"},
            {"'" + user.occupation + "'"},
            {"'" + user.interest + "'"},
            {user.playstyle},
            {user.playmode},
            {'false' if not user.is_subscriber else 'true'},
            {"'" + user.subscription_expires.strftime('%Y-%m-%d') + "'"},
            'bot'
        )
        '''
    cursor.execute(command)
    connection.commit()
    cursor.close()
    connection.close()


def update_user_in_database(user: OsuUser):
    """Update an OsuUser in the database"""
    # Import the database connection locally to avoid circular imports
    from utility.osu_database.utils import get_connection
    print(user.__dict__)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    command = f'''
        UPDATE phpbb_users SET
            user_regdate={int(user.register_date.timestamp())},
            username={"'" + user.username + "'"},
            username_clean={"'" + user.username_clean + "'"},
            user_email={"'" + user.email + "'"},
            user_lastvisit={int(user.last_visit.timestamp())},
            user_avatar={"'" + user.avatar + "'"},
            user_sig={"'" + user.signature + "'"},
            user_from={"'" + user.come_from + "'"},
            country_acronym={"'" + user.country_acronym + "'"},
            user_twitter={"'" + user.twitter + "'"},
            user_website={"'" + user.website + "'"},
            user_occ={"'" + user.occupation + "'"},
            user_interests={"'" + user.interest + "'"},
            osu_playstyle={user.playstyle},
            osu_playmode={user.playmode},
            osu_subscriber={'false' if not user.is_subscriber else 'true'},
            osu_subscriptionexpiry={"'" + user.subscription_expires.strftime('%Y-%m-%d') + "'" if user.subscription_expires else 'NULL'},
            user_permissions=''
        WHERE user_id={user.user_id}
        '''
    cursor.execute(command)
    connection.commit()
    cursor.close()
    connection.close()


def create_score_from_database_row(db_row: tuple) -> Score:
    """Create a Score from a database row"""
    return Score(
        database_id=db_row[0],
        user_id=db_row[1],
        beatmap_id=db_row[2],
        ruleset_id=db_row[3],
        data=db_row[4],
        has_replay=bool(db_row[5]),
        preserve=bool(db_row[6]),
        created_at=datetime.fromtimestamp(db_row[7]),
        updated_at=datetime.fromtimestamp(db_row[8])
    )


def create_beatmapset_from_database_row(db_row: tuple) -> BeatmapSet:
    """Create a Beatmapset from a database row"""
    return BeatmapSet(
        beatmapset_id=db_row[0],
        user_id=db_row[1],
        artist=db_row[3],
        artist_unicode=db_row[4],
        title=db_row[5],
        title_unicode=db_row[6],
        creator=db_row[7],
        source=db_row[8],
        tags=db_row[9],
        video=bool(db_row[10]),
        storyboard=bool(db_row[11]),
        epilepsy=bool(db_row[12]),
        bpm=db_row[13],
        approved=db_row[15],
        approved_date=db_row[17],
        submit_date=db_row[18],
        last_update=db_row[19],
        display_title=db_row[24],
        genre_id=db_row[25],
        language_id=db_row[26],
        download_disabled=bool(db_row[32]),
        favorite_count=db_row[36],
        play_count=db_row[37],
        difficulty_names=db_row[38]
    )


def insert_beatmapset_object_to_database(beatmapset: BeatmapSet):
    # Import the database connection locally to avoid circular imports
    from utility.osu_database.utils import get_connection
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    # Check artist, artist_unicode, title, title_unicode, creator, source, tags,
    # display_title that if it has ' in it, replace it with '' since SQL don't like '
    beatmapset.artist = beatmapset.artist.replace("'", "''") if beatmapset.artist else None
    beatmapset.artist_unicode = beatmapset.artist_unicode.replace("'", "''") if beatmapset.artist_unicode else None
    beatmapset.title = beatmapset.title.replace("'", "''") if beatmapset.title else None
    beatmapset.title_unicode = beatmapset.title_unicode.replace("'", "''") if beatmapset.title_unicode else None
    beatmapset.creator = beatmapset.creator.replace("'", "''") if beatmapset.creator else None
    beatmapset.source = beatmapset.source.replace("'", "''") if beatmapset.source else None
    beatmapset.tags = beatmapset.tags.replace("'", "''") if beatmapset.tags else None
    beatmapset.display_title = beatmapset.display_title.replace("'", "''") if beatmapset.display_title else None
    command = f'''
        INSERT INTO osu_beatmapsets (
            beatmapset_id,
            user_id,
            {f'artist,' if beatmapset.artist else ''}{f'artist_unicode,' if beatmapset.artist_unicode else ''}
            {f'title,' if beatmapset.title else ''}{f'title_unicode,' if beatmapset.title_unicode else ''}
            {f'creator,' if beatmapset.creator else ''}{f'source,' if beatmapset.source else ''}{f'tags,' if beatmapset.tags else ''}
            video,
            storyboard,
            epilepsy,
            bpm,
            approved,
            approved_date,
            submit_date,
            last_update,
            {f'displaytitle,' if beatmapset.display_title else ''}
            genre_id,
            language_id,
            download_disabled,
            favourite_count,
            play_count{f',difficulty_names' if beatmapset.difficulty_names else ''}
        ) VALUES (
            {beatmapset.beatmapset_id},
            {beatmapset.user_id},
            {"" if not beatmapset.artist else "'" + beatmapset.artist + "',"}{'' if not beatmapset.artist_unicode else "'" + beatmapset.artist_unicode + "',"}
            {"" if not beatmapset.title else "'" + beatmapset.title + "',"}{'' if not beatmapset.title_unicode else "'" + beatmapset.title_unicode + "',"}
            {"" if not beatmapset.creator else "'" + beatmapset.creator + "',"}{'' if not beatmapset.source else "'" + beatmapset.source + "',"}{'' if not beatmapset.tags else "'" + beatmapset.tags + "',"}
            {'false' if not beatmapset.video else 'true'},
            {'false' if not beatmapset.storyboard else 'true'},
            {'false' if not beatmapset.epilepsy else 'true'},
            {beatmapset.bpm},
            {beatmapset.approved},
            {"'" + str(beatmapset.approved_date) + "'" if beatmapset.approved_date else 'NULL'},
            {"'" + str(beatmapset.submit_date) + "'" if beatmapset.submit_date else 'NULL'},
            {"'" + str(beatmapset.last_update) + "'" if beatmapset.last_update else 'NULL'},
            {"" if not beatmapset.display_title else "'" + beatmapset.display_title + "',"}
            {beatmapset.genre_id},
            {beatmapset.language_id},
            {'false' if not beatmapset.download_disabled else 'true'},
            {beatmapset.favorite_count},
            {beatmapset.play_count}{'' if beatmapset.difficulty_names == '' else ',' + beatmapset.difficulty_names}
        )'''
    cursor.execute(command)
    connection.commit()
    cursor.close()
    connection.close()


def update_beatmapset_object_in_database(beatmapset: BeatmapSet):
    # Import the database connection locally to avoid circular imports
    from utility.osu_database.utils import get_connection
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    # Check artist, artist_unicode, title, title_unicode, creator, source, tags,
    # display_title that if it has ' in it, replace it with '' since SQL don't like '
    beatmapset.artist = beatmapset.artist.replace("'", "''") if beatmapset.artist else None
    beatmapset.artist_unicode = beatmapset.artist_unicode.replace("'", "''") if beatmapset.artist_unicode else None
    beatmapset.title = beatmapset.title.replace("'", "''") if beatmapset.title else None
    beatmapset.title_unicode = beatmapset.title_unicode.replace("'", "''") if beatmapset.title_unicode else None
    beatmapset.creator = beatmapset.creator.replace("'", "''") if beatmapset.creator else None
    beatmapset.source = beatmapset.source.replace("'", "''") if beatmapset.source else None
    beatmapset.tags = beatmapset.tags.replace("'", "''") if beatmapset.tags else None
    beatmapset.display_title = beatmapset.display_title.replace("'", "''") if beatmapset.display_title else None
    command = f'''
        UPDATE osu_beatmapsets
        SET
            user_id = {beatmapset.user_id},
            {'' if not beatmapset.artist else "artist = '" + beatmapset.artist + "',"}{'' if not beatmapset.artist_unicode else "artist_unicode = '" + beatmapset.artist_unicode + "',"}
            {'' if not beatmapset.title else "title = '" + beatmapset.title + "',"}{'' if not beatmapset.title_unicode else "title_unicode = '" + beatmapset.title_unicode + "',"}
            {'' if not beatmapset.creator else "creator = '" + beatmapset.creator + "',"}{'' if not beatmapset.source else "source = '" + beatmapset.source + "',"}
            {'' if not beatmapset.tags else "tags = '" + beatmapset.tags + "',"}
            video = {'false' if not beatmapset.video else 'true'},
            storyboard = {'false' if not beatmapset.storyboard else 'true'},
            epilepsy = {'false' if not beatmapset.epilepsy else 'true'},
            bpm = {beatmapset.bpm},
            approved = {beatmapset.approved},
            approved_date = {"'" + str(beatmapset.approved_date) + "'" if beatmapset.approved_date else 'NULL'},
            submit_date = {"'" + str(beatmapset.submit_date) + "'"},
            last_update = {"'" + str(beatmapset.last_update) + "'"},
            {'' if not beatmapset.display_title else "displaytitle = '" + beatmapset.display_title + "',"}
            genre_id = {beatmapset.genre_id},
            language_id = {beatmapset.language_id},
            download_disabled = {'false' if not beatmapset.download_disabled else 'true'},
            favourite_count = {beatmapset.favorite_count},
            play_count = {beatmapset.play_count}{'' if beatmapset.difficulty_names == '' else ',difficulty_names = ' + beatmapset.difficulty_names}
        WHERE beatmapset_id = {beatmapset.beatmapset_id}
        '''
    cursor.execute(command)
    connection.commit()
    cursor.close()
    connection.close()


def create_beatmap_from_database_row(db_row: tuple) -> Beatmap:
    """Create a Beatmap from a database row"""
    return Beatmap(
        beatmap_id=db_row[0],
        beatmapset_id=db_row[1],
        user_id=db_row[2],
        filename=db_row[3],
        checksum=db_row[4],
        version=db_row[5],
        total_length=db_row[6],
        hit_length=db_row[7],
        count_total=db_row[8],
        count_normal=db_row[9],
        count_slider=db_row[10],
        count_spinner=db_row[11],
        diff_drain=db_row[12],
        diff_size=db_row[13],
        diff_overall=db_row[14],
        diff_approach=db_row[15],
        play_mode=db_row[16],
        approved=db_row[17],
        last_update=db_row[18],
        difficulty_rating=db_row[19],
        play_count=db_row[20],
        pass_count=db_row[21],
        bpm=db_row[26]
    )


def insert_beatmap_object_to_database(beatmap: Beatmap):
    # Import the database connection locally to avoid circular imports
    from utility.osu_database.utils import get_connection
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    # Check filename, version that if it has ' in it, replace it with '' since SQL don't like '
    beatmap.filename = beatmap.filename.replace("'", "''") if beatmap.filename else None
    beatmap.version = beatmap.version.replace("'", "''") if beatmap.version else None
    command = f'''INSERT INTO osu_beatmaps (
            beatmap_id,
            beatmapset_id,
            user_id,
            filename,
            checksum,
            version,
            total_length,
            hit_length,
            countTotal,
            countNormal,
            countSlider,
            countSpinner,
            diff_drain,
            diff_size,
            diff_overall,
            diff_approach,
            playmode,
            approved,
            last_update,
            difficultyrating,
            playcount,
            passcount,
            bpm
        ) VALUES (
            {beatmap.beatmap_id},
            {beatmap.beatmapset_id},
            {beatmap.user_id},
            {"'" + beatmap.filename + "'"},
            {"'" + beatmap.checksum + "'"},
            {"'" + beatmap.version + "'"},
            {beatmap.total_length},
            {beatmap.hit_length},
            {beatmap.count_total},
            {beatmap.count_normal},
            {beatmap.count_slider},
            {beatmap.count_spinner},
            {beatmap.diff_drain},
            {beatmap.diff_size},
            {beatmap.diff_overall},
            {beatmap.diff_approach},
            {beatmap.play_mode},
            {beatmap.approved},
            {"'" + str(beatmap.last_update) + "'"},
            {beatmap.difficulty_rating},
            {beatmap.play_count},
            {beatmap.pass_count},
            {beatmap.bpm}
        )'''
    cursor.execute(command)
    connection.commit()
    cursor.close()
    connection.close()


def update_beatmap_object_in_database(beatmap: Beatmap):
    # Import the database connection locally to avoid circular imports
    from utility.osu_database.utils import get_connection
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('USE osu')
    # Check filename, version that if it has ' in it, replace it with '' since SQL don't like '
    beatmap.filename = beatmap.filename.replace("'", "''") if beatmap.filename else None
    beatmap.version = beatmap.version.replace("'", "''") if beatmap.version else None
    command = f'''
        UPDATE osu_beatmaps
        SET
            beatmapset_id = {beatmap.beatmapset_id},
            user_id = {beatmap.user_id},
            {'' if not beatmap.filename else "filename = '" + beatmap.filename + "',"}
            checksum = {"'" + beatmap.checksum + "'"},
            {'' if not beatmap.version else "version = '" + beatmap.version + "',"}
            total_length = {beatmap.total_length},
            hit_length = {beatmap.hit_length},
            countTotal = {beatmap.count_total},
            countNormal = {beatmap.count_normal},
            countSlider = {beatmap.count_slider},
            countSpinner = {beatmap.count_spinner},
            diff_drain = {beatmap.diff_drain},
            diff_size = {beatmap.diff_size},
            diff_overall = {beatmap.diff_overall},
            diff_approach = {beatmap.diff_approach},
            playmode = {beatmap.play_mode},
            approved = {beatmap.approved},
            last_update = {"'" + str(beatmap.last_update) + "'"},
            difficultyrating = {beatmap.difficulty_rating},
            playcount = {beatmap.play_count},
            passcount = {beatmap.pass_count},
            bpm = {beatmap.bpm}
        WHERE beatmap_id = {beatmap.beatmap_id}
        '''
    cursor.execute(command)
    connection.commit()
    cursor.close()
    connection.close()
