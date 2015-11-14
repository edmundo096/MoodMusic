from flask import *
from werkzeug import secure_filename
import os
import DbFunct

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTTEaSDFQ'
UPLOAD_FOLDER = './static/images/userprofile'
ALLOWED_EXTENSIONS = set([ 'png','jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def start():
	session['playlist']=[]
	return redirect(url_for('accueil'))
	
@app.route('/register', methods=['GET'])
def register():
	return render_template('register.html')
	
@app.route('/register', methods=['POST'])
def register_post():
	first_name = escape(request.form['pseudo'])
	email = escape(request.form['email'])
	password = escape(request.form['password'])
	user=DbFunct.recupUtilisateur(email, None)
	if user is None:
		DbFunct.insertUser(first_name, email, password)
		return redirect('/authent')
	else:
		return render_template('register.html')
@app.route('/top_music')
def top_music():
	email = session['email']
	liste = DbFunct.listTopMusicAll()
	return render_template('top.html', list_music = liste, pseudo=session['pseudo'])
@app.route('/last_music')
def last_music():
	liste = DbFunct.lastMusic()
	return render_template('last.html', list_music = liste, pseudo=session['pseudo'])
@app.route('/authent')
def page_authent():
	if 'email' in session:
		return redirect(url_for('accueil'))
	else:
		return render_template('authent.html')

@app.route('/submit_password', methods=['POST'])
def submit_psswd():
	if not request.json:
		abort(300)
	email = session['email']
	password = request.json['psswd']
	DbFunct.updatePassword(password, email)
	return jsonify({'succes':1})


@app.route('/login',methods=['POST'])
def login():
	user=DbFunct.recupUtilisateur(escape(request.form['email']),escape(request.form['password']))
	if user is None:
		return redirect(url_for('page_authent'))
	else:
		session['pseudo'] = user['pseudo']
		session['email'] =user['email']
		session['password']=user['password']
		session['playlist']=[]
		return redirect(url_for('accueil'))
		
		
@app.route('/accueil', methods=['GET'])
def accueil():
	if 'pseudo' in session:
		if not session['playlist']:
			for music in DbFunct.listeMusique():
				session['playlist'].append(json.dumps(music.nomArtist+" - "+music.nomAlbum+" - "+music.titre).replace('"',"" ))
		liste = session['playlist']
		if (request.args.get('compositeur') or request.args.get('titre')) is None:
			music=DbFunct.recupMusique(liste[0].split(" - ")[0], liste[0].split(" - ")[1],liste[0].split(" - ")[2])
		else:
			music=DbFunct.recupMusique(request.args.get('compositeur'), request.args.get('album'), request.args.get('titre'))
		return render_template('accueil.html', music=music, musiqueliste=liste, pseudo=session['pseudo'])
	else:
		return redirect(url_for('page_authent'))

@app.route('/api/getMusic', methods=['POST'])
def getMusic():
	if not request.json:
		abort(300)
	music = DbFunct.recupMusique(request.json['music'].split(" - ")[0], request.json['music'].split(" - ")[1], request.json['music'].split(" - ")[2])
	return jsonify({'Artist':music.nomArtist, 'Album': music.nomAlbum, 'Titre': music.titre, 'Annee': music.Annee, 'Label': music.Label, 'musicPath': music.musicPath, 'imagePath': music.imagePath})

@app.route('/accueil', methods=['POST'])
def chercher():
	if 'pseudo' in session:
		if request.form['search'] is not None:
			recherche=escape(request.form['search']).encode("utf-8")
			print recherche
			listeMotCle=recherche.split()
			session['playlist']=[]
			if not listeMotCle:
				return redirect("/accueil") 
			if (listeMotCle[0]!="humeur:"):
				listMusic=DbFunct.chercherMusique(listeMotCle)
			else:
				listMusic=DbFunct.algoMatch(listeMotCle[1:],session['email'])
			for music in listMusic:
				session['playlist'].append(json.dumps(music.nomArtist+" - "+music.nomAlbum+" - "+music.titre).replace('"',"" ))
				print session['playlist']
			listeMusiques=session['playlist']
			if not listeMusiques:
				return redirect("/accueil") 
			else:
				music=None
				music=DbFunct.recupMusique(listeMusiques[0].split(" - ")[0], listeMusiques[0].split(" - ")[1],listeMusiques[0].split(" - ")[2])
				return render_template('accueil.html', music=music, musiqueliste=listeMusiques, pseudo=session['pseudo'])
		else:
			return redirect("/accueil") 
	else:
		return redirect(url_for('page_authent'))
@app.route('/api/note', methods=['POST'])
def rating():
	if not request.json:
		abort(300)
	email=session['email']
	music=DbFunct.recupMusique(request.json['music'].split("-")[0],request.json['music'].split("-")[1], request.json['music'].split("-")[2])
	note=request.json['note']
	DbFunct.insererNote(email,music,note)
	return jsonify({'succes':1})		
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('page_authent'))
@app.route('/profile', methods=['GET', 'POST'])
def profile():
	liste = []
	liste = DbFunct.listTopMusicUser(session['email'])
	img = []
	img = DbFunct.getUserImage(session['email'])
	print img
	if request.method == 'GET':
		return render_template('profil.html', email=session['email'], pseudo=session['pseudo'], list_music = liste, image = img[0])
	
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		extension = filename.rsplit('.', 1)[1]
		filename = session['email']+'.'+extension
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		filename=  app.config['UPLOAD_FOLDER'].split(".")[1]+'/'+filename
		DbFunct.updateUserImage(filename, session['email'])
		return render_template('profil.html', email=session['email'], pseudo=session['pseudo'], list_music = liste, image=filename)
		
@app.route('/api/humeur', methods=['POST'])
def setHumeur():
	if not request.json:
		abort(300)
	email = session['email']
	music = DbFunct.recupMusique(request.json['music'].split("-")[0], request.json['music'].split("-")[1], request.json['music'].split("-")[2])
	humeur = request.json['humeur']
	DbFunct.insererHumeur(email, music, humeur)
	return jsonify({'succes':1})
		
		

if __name__ == '__main__':
  app.run(debug=True) 
