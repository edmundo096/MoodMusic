# useful set of functions for the server

import os
from sqlalchemy import *


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
    connection = engine.connect()
    return connection


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

    :returns: User object as {email, password, username, imagePath}.
    """
    connection = init()
    users = []
    if mdp is None:
        sql = "SELECT * FROM users WHERE users.email='" + email.encode("utf-8") + "'"
    else:
        sql = "SELECT * FROM users WHERE users.email='" + email.encode("utf-8") + "' AND users.password='" + mdp.encode(
            "utf-8") + "'"
    user = None
    for user in connection.execute(sql):
        users.append(user)
    return user


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

    :returns: String of the user image_path.
    :rtype: str
    """
    connection = init()
    sql = "SELECT imagePath FROM users WHERE users.email='" + email.encode("utf-8") + "'"
    picture = []
    for img in connection.execute(sql):
        picture = img
    return picture


# ----------------------------------------
# Songs handling
# ----------------------------------------

def listMusicYoutube():
    """
    Returns the list of Music.
    """
    connection = init()
    list = []
    sql = "SELECT Music.artist, Music.title, Music.album FROM Music WHERE Music.source = 'youtube'"
    for music in connection.execute(sql):
        print music
        list.append(music)
    return list


def get_song_data(artist, album, title):
    """Get a song data from the DB
    Returns an object with the properties: idmusic, title, musicPath, album, label, year, artist, imagePath.
    """
    connection = init()
    list = []
    sql = "SELECT Music.idmusic, Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music WHERE Music.title = '" + title.encode(
        "utf-8") + "' AND Music.artist = '" + artist.encode(
        "utf-8") + "' AND Music.album = '" + album.encode("utf-8") + "' AND Music.source = 'youtube'"

    for music in connection.execute(sql):
        list.append(music)
        # TODO Currently returns the last one form the list of the DB query.

    print "recupMusiqueYoutube list: {list}".format(list=list)

    # return music
    if len(list) > 0:
        return list[0]
    else:
        return None


def lastMusic():
    """
    return the list of last songs
    (But only the ones that are classified at least 1 time by any user, in other words, that exists on the rates table)
    Ordered by the Album Year in Descendent.
    """
    connection = init()
    list = []
    i = 0
    sql = "SELECT Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND Music.source = 'youtube' ORDER BY Music.year DESC"
    for m in connection.execute(sql):
        if i == 10:
            break
        list.append(m)
        i += 1
    return list


def listTopMusicAll():
    """
    return the list of top Music ordred by rating of users
    (But only the ones that are classified at least 1 time by any user, in other words, that exists on the rates table)
    """
    connection = init()
    list = []
    i = 0
    sql = "SELECT Music.title, Music.artist, Music.album, Music.imagePath, Music.musicPath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND Music.source = 'youtube' ORDER BY rates.rating DESC"
    for m in connection.execute(sql):
        if i == 10:
            break
        list.append(m)
        i += 1
    return list


def algoMatchYoutube(listMood, email):
    """function that gets music according to a specific mood set by the User email """
    connection = init()
    listGenre = []
    listAppGenre = []
    nbMusic = 0
    for Mood in listMood:
        sql = "SELECT Music.genre FROM Music, rates WHERE Music.idmusic = rates.idmusic AND rates.useremail = '" + email.encode(
            "utf-8") + "' AND rates.mood LIKE '%%" + Mood.encode("utf-8") + "%%' AND Music.source = 'youtube'"
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
                    sql = "SELECT Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music WHERE Music.genre LIKE '%%" + genre + "%%' AND Music.source = 'youtube'"
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


def insertMood(email, music, mood):
    """insert a mood to a song """
    connection = init()
    rates = []
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


def searchMusicYoutube(listKeyword):
    """Music search """
    connection = init()
    listMusic = []
    for keyword in listKeyword:
        sql = "SELECT Music.album, Music.artist, music.label, music.year, Music.title FROM Music WHERE (Music.title LIKE '%%" + keyword + "%%' OR Music.artist LIKE '%%" + keyword + "%%' OR Music.album LIKE '%%" + keyword + "%%' OR Music.label LIKE '%%" + keyword + "%%' OR Music.year LIKE '%%" + keyword + "%%') AND  Music.source = 'youtube'"
        for music in connection.execute(sql):
            if music in listMusic:
                pass
            else:
                print music
                listMusic.append(music)
    return listMusic


def insertRating(email, music, rating):
    """insert a rating to a song """
    connection = init()
    rates = []
    sql = "SELECT * FROM rates WHERE rates.useremail='" + email.encode("utf-8") + "' AND rates.idmusic=" + str(
        music.idmusic)
    for rate in connection.execute(sql):
        rates.append(rate)
    if not rates:
        sql = "INSERT INTO rates SET useremail='" + email.encode("utf-8") + "', idmusic=" + str(
            music.idmusic) + ", rating=" + rating
        connection.execute(sql)
    else:
        sql = "UPDATE rates SET rating=" + rating + " WHERE id=" + str(rates[0].id)
        connection.execute(sql)


def listTopMusicUser(email):
    """
    user favorite songs
    (Only the ones that are classified at least 1 time by the user)
    """
    connection = init()
    i = 0
    list = []
    sql = "SELECT Music.title, Music.artist, Music.album, Music.imagePath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND rates.useremail = '" + email.encode(
        "utf-8") + "' AND Music.source = 'youtube' ORDER BY rates.rating DESC"
    for m in connection.execute(sql):
        if i == 3:
            break
        list.append(m)
        i += 1
    return list



