# useful set of functions for the server

import os
from sqlalchemy import *

import config

engine = None

def init():
    global engine

    # Create the engine and connect to the DB if not exits.
    if engine == None:
        db_url = config.db_url

        # Check if the heroku local DB_URL var exist, then use it. (If the app runs on Heroku, use the ClearDB database).
        if os.environ.has_key('CLEARDB_DATABASE_URL'):
            # TODO: delete the '?reconnect=true' and add '+pymysql' and '?charset=utf8' from the default heroku var.
            # Should return this: mysql+pymysql://b6a232d03633eb:15c6e6ed@us-cdbr-iron-east-03.cleardb.net/heroku_f937bd33ab8f703?charset=utf8
            db_url = os.environ['CLEARDB_DATABASE_URL']

        print "DB_FUNCT: " + str(os.environ.has_key('CLEARDB_DATABASE_URL'))
        print "DB_FUNCT: " + db_url

        # Conn timeout of ClearDB is around 90,80 secs.
        engine = create_engine(db_url, echo=False, pool_recycle=80, pool_size=5, max_overflow=8)

        metadata = MetaData(engine)

    try:
        connection = engine.connect()
    except Exception, ex:
        print "\n*** Could NOT connect to the Data Base! ***\n" \
              "Check that the MySQL service is running and the 'db_url' is correct.\n"
        raise ex

    #connection = engine.connect()
    return connection


# ----------------------------------------
# User handling
# ----------------------------------------

def user_user_insert(username_u, email_u, password_u):
    """
    Insert a new User, using his username, email address, and password.
    """
    connection = init()
    sql = text("INSERT INTO users SET email=:email, password=:password, username=:username")
    connection.execute(sql, email=email_u, password=password_u, username=username_u)
    connection.close()


def user_user_get(email, mdp):
    """
    Get an User, using email, and optionally, a hashed password.

    :returns: Object as {email, password, username, imagePath}, if not found then None.
    :rtype: sqlalchemy.engine.result.RowProxy
    """
    connection = init()
    users = []
    if mdp is None:
        sql = text("SELECT * FROM users WHERE users.email=:email")
    else:
        sql = text("SELECT * FROM users WHERE users.email=:email AND users.password=:password")

    results = connection.execute(sql, email=email, password=mdp)

    return results.first()


def user_password_update(password, email):
    """
    Update the password, from an existing User.
    """
    connection = init()
    sql = text("UPDATE users SET password=:password WHERE users.email=:email")
    connection.execute(sql, password=password, email=email)
    connection.close()


def user_image_update(image_path, email):
    """
    Update the profile image_path, from an existent User.
    """
    connection = init()
    sql = text("UPDATE users SET imagePath=:imagePath WHERE users.email=:email")
    connection.execute(sql, imagePath=image_path, email=email)
    connection.close()


def user_image_get(email):
    """
    Get the profile image_path, from an existing User.

    :returns: String of the user image_path, if not found then None.
    :rtype: str
    """
    connection = init()
    sql = text("SELECT imagePath FROM users WHERE users.email=:email")

    # Since email is Primary key, should always return 1 row result.
    results_img = connection.execute(sql, email=email)

    # Doc: http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy
    # first() Returns None if no row is present.
    first_row = results_img.first()

    connection.close()
    if first_row is not None:
        # Return the imagePath from the first_row (either with first_row.imagePath or first_row[0]).
        return first_row.imagePath
    else:
        return None


# ----------------------------------------
# Songs handling
# ----------------------------------------

def song_songs_get_all(random = None, limit = None, source ='youtube'):
    """
    Get an Array of all songs in DB matching the source.
    If random is True, then ORDER BY Rand() is used, default is None.
    If limit is not None (a number), then LIMIT is used, default is None.
    Default source is 'youtube'.

    :returns: An Object Array of matched songs, each as {artist, title, album}.
    """
    connection = init()
    list = []
    sql = "SELECT Music.artist, Music.title, Music.album FROM Music WHERE Music.source = :source"

    if random:
        sql += " ORDER BY RAND()"

    if limit is not None:
        sql += " LIMIT :limit"

    sql = text(sql)

    for music_result_row in connection.execute(sql, source=source, limit=limit):
        list.append(music_result_row)

    connection.close()
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
    sql = text("SELECT Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music WHERE Music.source = :source ORDER BY Music.year DESC")

    for m in connection.execute(sql, source=source):
        if i == 10:
            break
        list.append(m)
        i += 1

    connection.close()
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
    sql = text("SELECT Music.title, Music.artist, Music.album, Music.imagePath, Music.musicPath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND Music.source = :source ORDER BY rates.rating DESC")

    for m in connection.execute(sql, source=source):
        if i == 10:
            break
        list.append(m)
        i += 1

    connection.close()
    return list


def song_songs_get_top_personal(email, source = 'youtube'):
    """
    Get an Array of the favorite, first 3 top User rated songs in DB, i.e. ordered by Decedent Rating, matching the source.

    :returns: An Object Array of matched songs, each as {title, artist, album, imagePath}.
    """
    connection = init()
    i = 0
    list = []
    sql = text("SELECT Music.title, Music.artist, Music.album, Music.imagePath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND rates.useremail = :email AND Music.source = :source ORDER BY rates.rating DESC")

    for m in connection.execute(sql, email=email, source=source):
        if i == 3:
            break
        list.append(m)
        i += 1

    connection.close()
    return list


def song_songs_get_with_mood(selected_moods, email, source = 'youtube'):
    """
    Get an Array of songs, ordered by Decedent Rating, matching the source and the Moods, already mood rated by the User email

    :returns: An Object Array of matched songs, each as {rating, idmusic, title, artist, album, year, label, source, imagePath, musicPath, genre, dateAdded}.
    """
    connection = init()
    song_rows_list = []

    for mood in selected_moods:
        sql = text("SELECT Music.*, rates.rating FROM Music, rates WHERE Music.idmusic = rates.idmusic AND rates.useremail = :email AND rates.mood LIKE :mood AND Music.source = :source")

        for result_row_song in connection.execute(sql, email=email, mood="%%{m}%%".format(m=mood), source=source):
            song_rows_list.append(result_row_song)

    connection.close()
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
        sql = text("SELECT Music.genre FROM Music, rates WHERE Music.idmusic = rates.idmusic AND rates.useremail = :email AND rates.mood LIKE :mood AND Music.source = :source")

        for listSQLGenre in connection.execute(sql, email=email, mood="%%{m}%%".format(m=mood), source=source):
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

            # TODO: This query is NOT SQL injection checked (since can be multiple parameters)
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

    connection.close()
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
        sql = text("SELECT Music.album, Music.artist, music.label, music.year, Music.title FROM Music WHERE (Music.title LIKE :keyword OR Music.artist LIKE :keyword OR Music.album LIKE :keyword OR Music.label LIKE :keyword OR Music.year LIKE :keyword) AND  Music.source = :source")
        for music in connection.execute(sql, keyword="%%{k}%%".format(k=keyword), source=source):
            if music in listMusic:
                pass
            else:
                listMusic.append(music)

    print "DB song_songs_get_with_search() results: " + str(listMusic)

    connection.close()
    return listMusic


def song_data_get(artist, album, title, source = 'youtube'):
    """
    Get a song with its data, from the specified artist, album, title, and source.
    Default source is 'youtube'.

    :returns: Object as {idmusic, title, musicPath, album, label, year, artist, imagePath}. None if no match found.
    :rtype: sqlalchemy.engine.result.RowProxy
    """
    connection = init()

    sql = text("SELECT Music.idmusic, Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music "
               "WHERE Music.title = :title AND Music.artist = :artist AND Music.album = :album AND Music.source = :source")

    # TODO Currently returns the first result (DB or function should be modified to only permit only 1 result, i.e. using a PK).
    results = connection.execute(sql, title=title, artist=artist, album=album, source=source)

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
    sql = text("SELECT * FROM users WHERE users.email=:email")
    if connection.execute(sql, email=email).first() == None:
        connection.close()
        return False

    sql = text("SELECT * FROM rates WHERE rates.useremail=:email AND rates.idmusic = :idmusic")
    for moodListResult in connection.execute(sql, email=email, idmusic=music.idmusic):
        rates.append(moodListResult)

    if not rates:
        sql = text("INSERT INTO rates SET useremail = :email, idmusic = :idmusic, mood = :mood")
        connection.execute(sql, email=email, idmusic=music.idmusic, mood=mood)
    else:
        sql = text("UPDATE rates SET mood=:mood WHERE id=:id")
        connection.execute(sql, mood=mood, id=rates[0].id)

    connection.close()
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
    sql = text("SELECT * FROM users WHERE users.email=:email")
    if connection.execute(sql, email=email).first() == None:
        connection.close()
        return False

    sql = text("SELECT * FROM rates, users WHERE rates.useremail=:email AND users.email = rates.useremail AND rates.idmusic=:idmusic")
    for rate in connection.execute(sql, email=email, idmusic=music.idmusic):
        rates.append(rate)

    if not rates:
        sql = text("INSERT INTO rates SET useremail=:email, idmusic=:idmusic, rating=:rating")
        connection.execute(sql, email=email, idmusic=music.idmusic, rating=rating)
    else:
        sql = text("UPDATE rates SET rating=" + rating + " WHERE id=:id")
        connection.execute(sql, id=rates[0].id)

    connection.close()
    return True
