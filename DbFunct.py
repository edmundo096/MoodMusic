# useful set of functions for the server

from sqlalchemy import *


def init():
    """Create the engine and connect to the DB"""
    engine = create_engine('mysql+pymysql://root:lok@localhost/web_db?charset=utf8', echo=False)
    metadata = MetaData(engine)
    connection = engine.connect()
    return connection


def insertUser(username_u, email_u, password_u):
    """insert the User using his username, email address and password """
    connection = init()
    sql = "INSERT INTO users SET email='" + email_u.encode("utf-8") + "', password='" + password_u.encode(
        "utf-8") + "', username='" + username_u.encode("utf-8") + "'"
    connection.execute(sql)


def updateUserImage(image, email):
    """set a new profile image for a user """
    connection = init()
    sql = "UPDATE users SET imagePath='" + image.encode("utf-8") + "' WHERE users.email='" + email.encode("utf-8") + "'"
    connection.execute(sql)


def recupUtilisateur(email, mdp):
    """get a User from the users table"""
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


def listeMusicYoutube():
    """Returns the list of Music  """
    connection = init()
    liste = []
    sql = "SELECT Music.artist, Music.title, Music.album FROM Music WHERE Music.source = 'youtube'"
    for music in connection.execute(sql):
        print music
        liste.append(music)
    return liste


def get_song_data(artist, album, title):
    """Get a song data from the DB
    Returns an object with the properties: idmusic, title, musicPath, album, label, year, artist, imagePath.
    """
    connection = init()
    liste = []
    sql = "SELECT Music.idmusic, Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music WHERE Music.title = '" + title.encode(
        "utf-8") + "' AND Music.artist = '" + artist.encode(
        "utf-8") + "' AND Music.album = '" + album.encode("utf-8") + "' AND Music.source = 'youtube'"

    for music in connection.execute(sql):
        liste.append(music)
        # TODO Currently returns the last one form the list of the DB query.

    print "recupMusiqueYoutube liste: {list}".format(list=liste)

    # return music
    if len(liste) > 0:
        return liste[0]
    else:
        return None


def updatePassword(password, email):
    """Update the user password """
    connection = init()
    sql = "UPDATE users SET password='" + password.encode("utf-8") + "' WHERE users.email='" + email.encode(
        "utf-8") + "'"
    connection.execute(sql)


def lastMusic():
    """
    return the list of last songs
    (But only the ones that are classified at least 1 time by any user, in other words, that exists on the rates table)
    Ordered by the Album Year in Descendent.
    """
    connection = init()
    liste = []
    i = 0
    sql = "SELECT Music.title, Music.musicPath, Music.album, Music.label, Music.year, Music.artist, Music.imagePath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND Music.source = 'youtube' ORDER BY Music.yearDESC"
    for m in connection.execute(sql):
        if i == 10:
            break
        liste.append(m)
        i += 1
    return liste


def listTopMusicAll():
    """
    return the list of top Music ordred by rating of users
    (But only the ones that are classified at least 1 time by any user, in other words, that exists on the rates table)
    """
    connection = init()
    liste = []
    i = 0
    sql = "SELECT Music.title, Music.artist, Music.album, Music.imagePath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND Music.source = 'youtube' ORDER BY rates.rating DESC"
    for m in connection.execute(sql):
        if i == 10:
            break
        liste.append(m)
        i += 1
    return liste


def algoMatchYoutube(listMood, email):
    """function that gets music according to a specific mood set by the User email """
    connection = init()
    listeGenre = []
    listeAppGenre = []
    nbMusic = 0;
    for Mood in listMood:
        sql = "SELECT Music.genre FROM Music, rates WHERE Music.idmusic = rates.idmusic AND rates.useremail = '" + email.encode(
            "utf-8") + "' AND rates.mood LIKE '%%" + Mood.encode("utf-8") + "%%' AND Music.source = 'youtube'"
        for listeSQLGenre in connection.execute(sql):
            nbMusic += 1
            for genre in listeSQLGenre.genre.split():
                if genre in listeGenre:
                    listeAppGenre[listeGenre.index(genre)] += 1
                else:
                    listeGenre.append(genre)
                    listeAppGenre.append(1)
    listeGenreImportant = []
    if nbMusic != 0:
        for genre in listeGenre:
            if listeAppGenre[listeGenre.index(genre)] / float(nbMusic) >= 0.5:
                listeGenreImportant.append(genre)
    playlist = []
    k = len(listeGenreImportant)
    while k > 0:
        i = 0
        while i + k <= len(listeGenreImportant):
            sql = ""
            for genre in listeGenreImportant[i:i + k]:
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


def searchMusicYoutube(listeKeyword):
    """Music search """
    connection = init()
    listeMusic = []
    for keyword in listeKeyword:
        sql = "SELECT Music.album, Music.artist, music.label, music.year, Music.title FROM Music WHERE (Music.title LIKE '%%" + keyword + "%%' OR Music.artist LIKE '%%" + keyword + "%%' OR Music.album LIKE '%%" + keyword + "%%' OR Music.label LIKE '%%" + keyword + "%%' OR Music.year LIKE '%%" + keyword + "%%') AND  Music.source = 'youtube'"
        for music in connection.execute(sql):
            if music in listeMusic:
                pass
            else:
                print music
                listeMusic.append(music)
    return listeMusic


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
            music.idmusic) + ", rating=" + rating;
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
    liste = []
    sql = "SELECT Music.title, Music.artist, Music.album, Music.imagePath FROM Music, rates WHERE rates.idmusic = Music.idmusic AND rates.useremail = '" + email.encode(
        "utf-8") + "' AND Music.source = 'youtube' ORDER BY rates.rating DESC"
    for m in connection.execute(sql):
        if i == 3:
            break
        liste.append(m)
        i += 1
    return liste


def getUserImage(email):
    """get the user image """
    connection = init()
    sql = "SELECT imagePath FROM users WHERE users.email='" + email.encode("utf-8") + "'"
    picture = []
    for img in connection.execute(sql):
        picture = img
    return picture
