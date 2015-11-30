# useful set of functions for the server

from sqlalchemy import *


def init():
    """Create the engine and connect to the DB"""
    engine = create_engine('mysql+pymysql://root:lok@localhost/web_db?charset=utf8', echo=False)
    metadata = MetaData(engine)
    connection = engine.connect()
    return connection


def insertUser(pseudo_u, email_u, password_u):
    """insert the User using his username, email address and password """
    connection = init()
    sql = "INSERT INTO users SET email='" + email_u.encode("utf-8") + "', password='" + password_u.encode(
        "utf-8") + "', pseudo='" + pseudo_u.encode("utf-8") + "'"
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


def listeMusiqueYoutube():
    """Returns the list of Music  """
    connection = init()
    liste = []
    sql = "SELECT Music.compositeur, Music.titre, Music.nomAlbum FROM Music WHERE Music.source = 'youtube'"
    for music in connection.execute(sql):
        print music
        liste.append(music)
    return liste


def recupMusiqueYoutube(compositeur, album, titre):
    """Get a song data from the DB"""
    connection = init()
    liste = []
    sql = "SELECT Music.idmusic, Music.titre, Music.musicPath, Music.nomAlbum, Music.label, Music.annee, Music.compositeur, Music.imagePath FROM Music WHERE Music.titre = '" + titre.encode(
        "utf-8") + "' AND Music.nomArtist = '" + compositeur.encode(
        "utf-8") + "' AND Music.nomAlbum = '" + album.encode("utf-8") + "' AND Music.source = 'youtube'"

    for music in connection.execute(sql):
        liste.append(music)
        # TODO Currently returns the last one form the list of the DB query.

    print "recupMusiqueYoutube liste: {lst}".format(lst=liste)

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
    (But only the ones that are classified at least 1 time by any user, in other words, that exists on the avis table)
    Ordered by the Album Year in Descendent.
    """
    connection = init()
    liste = []
    i = 0
    sql = "SELECT Music.titre, Music.musicPath, Music.nomAlbum, Music.label, Music.annee, Music.compositeur, Music.imagePath FROM Music, avis WHERE avis.idmusic = Music.idmusic AND Music.source = 'youtube' ORDER BY Music.annee DESC"
    for m in connection.execute(sql):
        if i == 10:
            break
        liste.append(m)
        i += 1
    return liste


def listTopMusicAll():
    """
    return the list of top Music ordred by note of users
    (But only the ones that are classified at least 1 time by any user, in other words, that exists on the avis table)
    """
    connection = init()
    liste = []
    i = 0
    sql = "SELECT Music.titre, Music.compositeur, Music.nomAlbum, Music.imagePath FROM Music, avis WHERE avis.idmusic = Music.idmusic AND Music.source = 'youtube' ORDER BY avis.note DESC"
    for m in connection.execute(sql):
        if i == 10:
            break
        liste.append(m)
        i += 1
    return liste


def algoMatchYoutube(listeHumeur, email):
    """function that gets music according to a specific mood set by the User email """
    connection = init()
    listeCaract = []
    listeAppCaract = []
    nbMusique = 0;
    for Humeur in listeHumeur:
        sql = "SELECT Music.caract FROM Music, avis WHERE Music.idmusic = avis.idmusic AND avis.useremail = '" + email.encode(
            "utf-8") + "' AND avis.humeur LIKE '%%" + Humeur.encode("utf-8") + "%%' AND Music.source = 'youtube'"
        for listeSQLCaract in connection.execute(sql):
            nbMusique += 1
            for caract in listeSQLCaract.caract.split():
                if caract in listeCaract:
                    listeAppCaract[listeCaract.index(caract)] += 1
                else:
                    listeCaract.append(caract)
                    listeAppCaract.append(1)
    listeCaractImportante = []
    if nbMusique != 0:
        for caract in listeCaract:
            if listeAppCaract[listeCaract.index(caract)] / float(nbMusique) >= 0.5:
                listeCaractImportante.append(caract)
    playlist = []
    k = len(listeCaractImportante)
    while k > 0:
        i = 0
        while i + k <= len(listeCaractImportante):
            sql = ""
            for caract in listeCaractImportante[i:i + k]:
                if sql == "":
                    sql = "SELECT Music.titre, Music.musicPath, Music.nomAlbum, Music.label, Music.annee, Music.compositeur, Music.imagePath FROM Music WHERE Music.caract LIKE '%%" + caract + "%%' AND Music.source = 'youtube'"
                else:
                    sql += " AND Music.caract LIKE '%%" + caract + "%%'"

            for music in connection.execute(sql):
                if music in playlist:
                    pass
                else:
                    playlist.append(music)
            i += 1
        k -= 1
    return playlist


def insererHumeur(email, music, humeur):
    """insert a mood to a song """
    connection = init()
    avis = []
    sql = "SELECT * FROM avis WHER avis.useremail='" + email.encode("utf-8") + "' AND avis.idmusic = " + str(
        music.idmusic)

    for hum in connection.execute(sql):
        avis.append(hum)

    if not avis:
        sql = "INSERT INTO avis SET useremail = '" + email.encode("utf-8") + "', idmusic = " + str(
            music.idmusic) + ", humeur = '" + humeur.encode("utf-8") + "'"
        connection.execute(sql)
    else:
        sql = "UPDATE avis SET humeur='" + humeur.encode("utf-8") + "' WHERE id=" + str(avis[0].id)
        connection.execute(sql)


def chercherMusiqueYoutube(listeMotCle):
    """Music search """
    connection = init()
    listeMusiques = []
    for motCle in listeMotCle:
        sql = "SELECT Music.nomAlbum, Music.compositeur, music.label, music.annee, Music.titre FROM Music WHERE (Music.titre LIKE '%%" + motCle + "%%' OR Music.compositeur LIKE '%%" + motCle + "%%' OR Music.nomAlbum LIKE '%%" + motCle + "%%' OR Music.label LIKE '%%" + motCle + "%%' OR Music.Annee LIKE '%%" + motCle + "%%') AND  Music.source = 'youtube'"
        for music in connection.execute(sql):
            if music in listeMusiques:
                pass
            else:
                print music
                listeMusiques.append(music)
    return listeMusiques


def insererNote(email, music, note):
    """insert a note to a song """
    connection = init()
    avis = []
    sql = "SELECT * FROM avis WHERE avis.useremail='" + email.encode("utf-8") + "' AND avis.idmusic=" + str(
        music.idmusic)
    for avi in connection.execute(sql):
        avis.append(avi)
    if not avis:
        sql = "INSERT INTO avis SET useremail='" + email.encode("utf-8") + "', idmusic=" + str(
            music.idmusic) + ", note=" + note;
        connection.execute(sql)
    else:
        sql = "UPDATE avis SET note=" + note + " WHERE id=" + str(avis[0].id)
        connection.execute(sql)


def listTopMusicUser(email):
    """
    user favorite songs
    (Only the ones that are classified at least 1 time by the user)
    """
    connection = init()
    i = 0
    liste = []
    sql = "SELECT Music.titre, Music.compositeur, Music.nomAlbum, Music.imagePath FROM Music, avis WHERE avis.idmusic = Music.idmusic AND avis.useremail = '" + email.encode(
        "utf-8") + "' AND Music.source = 'youtube' ORDER BY avis.note DESC"
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
