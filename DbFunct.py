''' useful set of functions for the server '''


from sqlalchemy import *

'''Create the engine and connect to the DB'''
def init():
    engine = create_engine('mysql+pymysql://root:lok@localhost/web_db?charset=utf8', echo=False)
    metadata = MetaData(engine)
    connection = engine.connect()
    return connection

'''insert the User using his username, email address and password '''

def insertUser(pseudo_u, email_u, password_u):
	connection = init()
	sql="INSERT INTO users set email='"+email_u.encode("utf-8")+"', password='"+password_u.encode("utf-8")+"', pseudo='"+pseudo_u.encode("utf-8")+"'"
	connection.execute(sql)

'''set a new profile image for a user '''
def updateUserImage(image, email):
	connection = init()
	sql = "UPDATE users SET imagePath='"+image.encode("utf-8")+"' WHERE users.email='"+email.encode("utf-8")+"'"
	connection.execute(sql)


'''get a User from the users table'''
def recupUtilisateur(email, mdp):
	connection=init()
	users=[]
	if mdp is None:
		sql="select * from users where users.email='"+email.encode("utf-8")+"'"
	else:
		sql="select * from users where users.email='"+email.encode("utf-8")+"' and users.password='"+mdp.encode("utf-8")+"'"
	user = None
	for user in connection.execute(sql):
		users.append(user)
	return user


'''Returns the list of Music  '''
def listeMusiqueYoutube():
    connection=init()
    liste=[]
    sql = "SELECT Music.compositeur, Music.titre, Music.nomAlbum FROM Music WHERE Music.source = 'youtube'"
    for music in connection.execute(sql):
        print music
        liste.append(music)
    return liste


'''Get a song data from the DB'''
def recupMusiqueYoutube(compositeur, album, titre):
    connection=init()
    liste=[]
    sql = "SELECT Music.idmusic, Music.titre, Music.musicPath, Music.nomAlbum, Music.label, Music.annee, Music.compositeur, Music.imagePath FROM Music WHERE Music.titre = '" + titre.encode("utf-8") + "' AND Music.nomArtist = '" + compositeur.encode("utf-8") + "' AND Music.nomAlbum = '" + album.encode("utf-8") + "' AND Music.source = 'youtube'"

    for music in connection.execute(sql):
        liste.append(music)
        # TODO Currently returns the last one form the list of the DB query.

    print "recupMusiqueYoutube liste: {lst}".format(lst=liste)

    #return music
    if len(liste) > 0:
        return liste[0]
    else:
        return None


'''Update the user password '''
def updatePassword(password, email):
	connection = init()
	sql = "UPDATE users SET password='"+password.encode("utf-8")+"' WHERE users.email='"+email.encode("utf-8")+"'"
	connection.execute(sql)

'''
return the list of last songs
(But only the ones that are classified at least 1 time by any user, in other words, that exists on the avis table)
Ordered by the Album Year in Descendent.
'''
def lastMusic():
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

'''
return the list of top Music ordred by note of users
(But only the ones that are classified at least 1 time by any user, in other words, that exists on the avis table)
'''
def listTopMusicAll():
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

'''function that gets music according to a specific mood set by the User email '''
def algoMatchYoutube(listeHumeur,email):
	connection=init()
	listeCaract=[]
	listeAppCaract=[]
	nbMusique=0;
	for Humeur in listeHumeur:
		sql ="SELECT Music.caract FROM Music, avis WHERE Music.idmusic = avis.idmusic AND avis.useremail = '" + email.encode("utf-8") + "' AND avis.humeur LIKE '%%" + Humeur.encode("utf-8") + "%%' AND Music.source = 'youtube'"
		for listeSQLCaract in connection.execute(sql):
			nbMusique+=1
			for caract in listeSQLCaract.caract.split():
				if caract in listeCaract:
					listeAppCaract[listeCaract.index(caract)]+=1
				else:
					listeCaract.append(caract)
					listeAppCaract.append(1)
	listeCaractImportante=[]
	if nbMusique!=0:
		for caract in listeCaract:
			if listeAppCaract[listeCaract.index(caract)]/float(nbMusique)>=0.5:
				listeCaractImportante.append(caract)
	playlist=[]
	k=len(listeCaractImportante)
	while k>0:
		i=0
		while i+k<=len(listeCaractImportante):
			sql=""
			for caract in listeCaractImportante[i:i+k]:
				if sql=="":
					sql = "SELECT Music.titre, Music.musicPath, Music.nomAlbum, Music.label, Music.annee, Music.compositeur, Music.imagePath FROM Music WHERE Music.caract LIKE '%%" + caract + "%%' AND Music.source = 'youtube'"
				else:
					sql += " AND Music.caract LIKE '%%" + caract + "%%'"

			for music in connection.execute(sql):
				if music in playlist:
					pass
				else:
					playlist.append(music)
			i+=1
		k-=1
	return playlist

'''insert a mood to a song '''
def insererHumeur(email, music, humeur):
	connection = init()
	avis = []
	sql = "SELECT * FROM avis WHER avis.useremail='" + email.encode("utf-8") + "' AND avis.idmusic = " + str(music.idmusic)

	for hum in connection.execute(sql):
		avis.append(hum)

	if not avis:
		sql = "INSERT INTO avis set useremail = '" + email.encode("utf-8") + "', idmusic = " + str(music.idmusic) + ", humeur = '" + humeur.encode("utf-8") + "'"
		connection.execute(sql)
	else:
		sql = "UPDATE avis set humeur='"+humeur.encode("utf-8")+"' where id="+str(avis[0].id)
		connection.execute(sql)

'''Music search '''
def chercherMusiqueYoutube(listeMotCle):
	connection=init()
	listeMusiques=[]
	for motCle in listeMotCle:
		sql = "SELECT Music.nomAlbum, Music.compositeur, music.label, music.annee, Music.titre from Music WHERE (Music.titre LIKE '%%"+motCle+"%%' or Music.compositeur LIKE '%%"+motCle+"%%' or Music.nomAlbum LIKE '%%"+motCle+"%%' or Music.label LIKE '%%"+motCle+"%%' or Music.Annee LIKE '%%"+motCle+"%%') AND  Music.source = 'youtube'"
		for music in connection.execute(sql):
			if music in listeMusiques:
				pass
			else:
				print music
				listeMusiques.append(music)
	return listeMusiques

'''insert a note to a song '''
def insererNote(email,music,note):
	connection=init()
	avis=[]
	sql="SELECT * from avis where avis.useremail='"+email.encode("utf-8")+"' and avis.idmusic="+str(music.idmusic)
	for avi in connection.execute(sql):
		avis.append(avi)
	if not avis:
		sql="INSERT INTO avis SET useremail='"+email.encode("utf-8")+"', idmusic="+str(music.idmusic)+", note="+note;
		connection.execute(sql)
	else:
		sql="UPDATE avis SET note="+note+" WHERE id="+str(avis[0].id)
		connection.execute(sql)

'''
user favorite songs
(Only the ones that are classified at least 1 time by the user)
'''
def listTopMusicUser(email):
	connection = init()
	i = 0
	liste = []
	sql = "SELECT Music.titre, Music.compositeur, Music.nomAlbum, Music.imagePath FROM Music, avis WHERE avis.idmusic = Music.idmusic AND avis.useremail = '"+email.encode("utf-8") + "' AND Music.source = 'youtube' ORDER BY avis.note DESC"
	for m in connection.execute(sql):
		if i == 3:
			break
		liste.append(m)
		i += 1
	return liste

'''get the user image '''
def getUserImage(email):
	connection = init()
	sql = "SELECT imagePath FROM users WHERE users.email='"+email.encode("utf-8")+"'"
	picture = []
	for img in connection.execute(sql):
		picture = img
	return picture

