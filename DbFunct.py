# useful set of functions for the server

import os
from sqlalchemy import *

privateConn = None

def init():
    """Create the engine and connect to the DB"""

    db_url = 'mysql+pymysql://root:lok@localhost/web_db?charset=utf8'

    # Check if the heroku local DB_URL var exist, then use it.
    # (If the app runs on Heroku, use the ClearDB database).
    if os.environ.has_key('CLEARDB_DATABASE_URL'):
        # Todo, delete the '?reconnect=true' and add '+pymysql' and '?charset=utf8' from the default heroku var.
        # Should return this: mysql+pymysql://b6a232d03633eb:15c6e6ed@us-cdbr-iron-east-03.cleardb.net/heroku_f937bd33ab8f703?charset=utf8
        db_url = os.environ['CLEARDB_DATABASE_URL']

    print "DB_FUNCT: " + str(os.environ.has_key('CLEARDB_DATABASE_URL'))
    print "DB_FUNCT: " + db_url

    engine = create_engine(db_url, echo=False)

    metadata = MetaData(engine)

    global privateConn
    if privateConn == None or privateConn.closed:
        privateConn = engine.connect()

    #connection = engine.connect()
    return privateConn


# ----------------------------------------
# User handling
# ----------------------------------------

def user_user_insert(username_u, email_u, password_u):
    """
    Insert a new User, using his username, email address, and password.
    """
    connection = init()
    sql = "INSERT INTO users SET email='" + email_u.encode("utf-8") + "', password='" + password_u.encode(
        "utf-8") + "', username='" + username_u.encode("utf-8") + "'"
    connection.execute(sql)


def user_user_get(email, mdp):
    """
    Get an User, using email, and optionally, a hashed password.

    :returns: Object as {email, password, username, imagePath}, if not found then None.
    :rtype: sqlalchemy.engine.result.RowProxy
    """
    connection = init()
    users = []
    if mdp is None:
        sql = "SELECT * FROM users WHERE users.email='" + email.encode("utf-8") + "'"
    else:
        sql = "SELECT * FROM users WHERE users.email='" + email.encode("utf-8") + "' AND users.password='" + mdp.encode(
            "utf-8") + "'"

    results = connection.execute(sql)
    return results.first()


def user_password_update(password, email):
    """
    Update the password, from an existing User.
    """
    connection = init()
    sql = "UPDATE users SET password='" + password.encode("utf-8") + "' WHERE users.email='" + email.encode(
        "utf-8") + "'"
    connection.execute(sql)


def user_image_update(image_path, email):
    """
    Update the profile image_path, from an existent User.
    """
    connection = init()
    sql = "UPDATE users SET imagePath='" + image_path.encode("utf-8") + "' WHERE users.email='" + email.encode("utf-8") + "'"
    connection.execute(sql)


def user_image_get(email):
    """
    Get the profile image_path, from an existing User.

    :returns: String of the user image_path, if not found then None.
    :rtype: str
    """
    connection = init()
    sql = "SELECT imagePath FROM users WHERE users.email='" + email.encode("utf-8") + "'"

    # Since email is Primary key, should always return 1 row result.
    results_img = connection.execute(sql)

    # Doc: http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy
    # first() Returns None if no row is present.
    first_row = results_img.first()

    if first_row is not None:
        # Return the imagePath from the first_row (either with first_row.imagePath or first_row[0]).
        return first_row.imagePath
    else:
        return None


# ----------------------------------------
# Songs handling
# ----------------------------------------

def song_songs_get_all(source ='youtube'):
    """
    Get an Array of all songs in DB matching the source.
    Default source is 'youtube'.

    :returns: An Object Array of matched songs, each as {artist, title, album}.
    """
    connection = init()
    list = []
    sql = "SELECT Music.artist, Music.title, Music.album FROM Music WHERE Music.source = '{s}'".format(s=source)

    for music_result_row in connection.execute(sql):
        list.append(music_result_row)

    return list


def song_songs_get_latest(source = 'youtube'):
    """
    Get an Array of the first 10 latest songs in DB, i.e. ordered by Decedent Year, matching the source.
    Default source is 'youtube'.

    :returns: An Object Array of matched songs, each as {title, musicPath, album, label, year, artist, imagePath}.
    """
    connection = init()
    list = []
    i = 0
    sql = "SELECT Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music WHERE Music.source = '{s}' ORDER BY Music.year DESC".format(s=source)
    for m in connection.execute(sql):
        if i == 10:
            break
        list.append(m)
        i += 1

    return list


def song_songs_get_top_global(source ='youtube'):
    """
    Get an Array of the first 10 top rated songs in DB, i.e. ordered by Decedent Rating, matching the source.
    (But only the ones that are classified at least 1 time by any user, in other words, that exists on the rates table)

    :returns: An Object Array of matched songs, each as {title, artist, album, imagePath}.
    """
    connection = init()
    list = []
    i = 0
    sql = "SELECT Music.title, Music.artist, Music.album, Music.imagePath, Music.musicPath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND Music.source = '{s}' ORDER BY rates.rating DESC".format(s=source)
    for m in connection.execute(sql):
        if i == 10:
            break
        list.append(m)
        i += 1

    return list


def song_songs_get_top_personal(email, source = 'youtube'):
    """
    Get an Array of the favorite, first 3 top User rated songs in DB, i.e. ordered by Decedent Rating, matching the source.

    :returns: An Object Array of matched songs, each as {title, artist, album, imagePath}.
    """
    connection = init()
    i = 0
    list = []
    sql = "SELECT Music.title, Music.artist, Music.album, Music.imagePath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND rates.useremail = '" + email.encode(
        "utf-8") + "' AND Music.source = '{s}' ORDER BY rates.rating DESC".format(s=source)
    for m in connection.execute(sql):
        if i == 3:
            break
        list.append(m)
        i += 1

    return list


def song_songs_get_with_mood(selected_moods, email, source = 'youtube'):
    """
    Get an Array of songs, ordered by Decedent Rating, matching the source and the Moods, already mood rated by the User email

    :returns: An Object Array of matched songs, each as {rating, idmusic, title, artist, album, year, label, source, imagePath, musicPath, genre, dateAdded}.
    """
    connection = init()
    song_rows_list = []

    for mood in selected_moods:
        sql = "SELECT Music.*, rates.rating FROM Music, rates WHERE Music.idmusic = rates.idmusic AND rates.useremail = '" + email.encode(
            "utf-8") + "' AND rates.mood LIKE '%%" + mood.encode("utf-8") + "%%' AND Music.source = '{s}'".format(s=source)
        for result_row_song in connection.execute(sql):
            song_rows_list.append(result_row_song)

    # Sort by ratings in descendant.
    return sorted(song_rows_list, key=lambda song: song.rating, reverse=True)


def song_songs_get_with_mood_genres(selected_moods, email, source = 'youtube'):
    """
    Get an Array of songs of similar gender with the gender of the specified Moods songs, already mood rated by the User email.

    :returns: An Object Array of matched songs, each as {title, musicPath, album, label, year, artist, imagePath}.
    """
    connection = init()
    listGenre = []
    listAppGenre = []
    nbMusic = 0

    for mood in selected_moods:
        sql = "SELECT Music.genre FROM Music, rates WHERE Music.idmusic = rates.idmusic AND rates.useremail = '" + email.encode(
            "utf-8") + "' AND rates.mood LIKE '%%" + mood.encode("utf-8") + "%%' AND Music.source = '{s}'".format(s=source)

        for listSQLGenre in connection.execute(sql):
            nbMusic += 1
            for genre in listSQLGenre.genre.split():
                if genre in listGenre:
                    listAppGenre[listGenre.index(genre)] += 1
                else:
                    listGenre.append(genre)
                    listAppGenre.append(1)

    listGenreImportant = []

    if nbMusic != 0:
        for genre in listGenre:
            if listAppGenre[listGenre.index(genre)] / float(nbMusic) >= 0.5:
                listGenreImportant.append(genre)

    playlist = []

    k = len(listGenreImportant)
    while k > 0:
        i = 0
        while i + k <= len(listGenreImportant):
            sql = ""
            for genre in listGenreImportant[i:i + k]:
                if sql == "":
                    sql = "SELECT Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music WHERE Music.genre LIKE '%%" + genre + "%%' AND Music.source = '{s}'".format(s=source)
                else:
                    sql += " AND Music.genre LIKE '%%" + genre + "%%'"

            for music in connection.execute(sql):
                if music in playlist:
                    pass
                else:
                    playlist.append(music)
            i += 1
        k -= 1

    return playlist


def song_songs_get_with_search(listKeyword, source = 'youtube'):
    """
    Music search.
    Get an Array of all songs in DB matching the source and the keywords with any of the following:
        title, artist, album, label, year.
    Default source is 'youtube'

    :returns: An Object Array of matched songs, each as {album, artist, label, year, title}.
    """
    connection = init()
    listMusic = []
    for keyword in listKeyword:
        sql = "SELECT Music.album, Music.artist, music.label, music.year, Music.title FROM Music WHERE (Music.title LIKE '%%" + keyword + "%%' OR Music.artist LIKE '%%" + keyword + "%%' OR Music.album LIKE '%%" + keyword + "%%' OR Music.label LIKE '%%" + keyword + "%%' OR Music.year LIKE '%%" + keyword + "%%') AND  Music.source = '{s}'".format(s=source)
        for music in connection.execute(sql):
            if music in listMusic:
                pass
            else:
                print music
                listMusic.append(music)

    return listMusic


def song_data_get(artist, album, title, source = 'youtube'):
    """
    Get a song with its data, from the specified artist, album, title, and source.
    Default source is 'youtube'.

    :returns: Object as {idmusic, title, musicPath, album, label, year, artist, imagePath}.
    :rtype: sqlalchemy.engine.result.RowProxy
    """
    connection = init()

    sql = "SELECT Music.idmusic, Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music WHERE Music.title = '" + title.encode(
        "utf-8") + "' AND Music.artist = '" + artist.encode(
        "utf-8") + "' AND Music.album = '" + album.encode("utf-8") + "' AND Music.source = '{s}'".format(s=source)

    # TODO Currently returns the first result (DB or function should be modified to only permit only 1 result, i.e. using a PK).
    results = connection.execute(sql)

    return results.first()


def song_rate_set_mood(email, music, mood):
    """
    Insert or Update a mood to a song, given an existing user email.

    :returns: Boolean, false if email does not exists on a user, true otherwise.
    :rtype: bool
    """
    connection = init()
    rates = []

    # Check if an user with that email does Not exists.
    sql = "SELECT * FROM users WHERE users.email='" + email.encode("utf-8") + "'"
    if connection.execute(sql).first() == None:
        return False

    sql = "SELECT * FROM rates WHERE rates.useremail='" + email.encode("utf-8") + "' AND rates.idmusic = " + str(
        music.idmusic)
    for moodListResult in connection.execute(sql):
        rates.append(moodListResult)

    if not rates:
        sql = "INSERT INTO rates SET useremail = '" + email.encode("utf-8") + "', idmusic = " + str(
            music.idmusic) + ", mood = '" + mood.encode("utf-8") + "'"
        connection.execute(sql)
    else:
        sql = "UPDATE rates SET mood='" + mood.encode("utf-8") + "' WHERE id=" + str(rates[0].id)
        connection.execute(sql)

    return True


def song_rate_set_rating(email, music, rating):
    """
    Insert or Update a rating to a song, given an existing user email.

    :returns: Boolean, false if email does not exists on a user, true otherwise.
    :rtype: bool
    """
    connection = init()
    rates = []

    # Check if an user with that email does Not exists.
    sql = "SELECT * FROM users WHERE users.email='" + email.encode("utf-8") + "'"
    if connection.execute(sql).first() == None:
        return False

    sql = "SELECT * FROM rates, users WHERE rates.useremail='" + email.encode(
        "utf-8") + "' AND users.email = rates.useremail AND rates.idmusic=" + str(music.idmusic)
    for rate in connection.execute(sql):
        rates.append(rate)

    if not rates:
        sql = "INSERT INTO rates SET useremail='" + email.encode("utf-8") + "', idmusic=" + str(
            music.idmusic) + ", rating=" + rating
        connection.execute(sql)
    else:
        sql = "UPDATE rates SET rating=" + rating + " WHERE id=" + str(rates[0].id)
        connection.execute(sql)

    return True
