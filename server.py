"""LTU SE M7011E Project Music Mood """

from flask import *
from werkzeug import secure_filename
import os
import DbFunct
import hashlib

app = Flask(__name__)

"""The key for the application"""
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTTEaSDFQ'

UPLOAD_FOLDER = './static/images/userprofile'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

"""app configuration*****"""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable HTTPS
import ssl

appPath = os.path.dirname(os.path.realpath(__file__))
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(appPath + '/ssl.crt', appPath + '/ssl.key')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def start():
    """  starting route """
    session['playlist'] = []
    return redirect(url_for('accueil'))


@app.route('/register', methods=['GET'])
def register():
    """Get the Registration page """
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    """Route to Post the user Information in the DB (making call to the insertUser function ) and redirect to the authentication page"""
    first_name = escape(request.form['pseudo'])
    email = escape(request.form['email'])
    password = escape(request.form['password'])
    # Encrypt password.
    password = hashlib.sha224(password).hexdigest()
    user = DbFunct.recupUtilisateur(email, None)
    if user is None:
        DbFunct.insertUser(first_name, email, password)
        return redirect('/authent')
    else:
        return render_template('register.html')


@app.route('/authent')
def page_authent():
    """authentication route for all users """
    if 'email' in session:
        return redirect(url_for('accueil'))
    else:
        return render_template('authent.html')


@app.route('/submit_password', methods=['POST'])
def submit_psswd():
    """route to submit the new password   """
    if not request.json:
        abort(300)
    email = session['email']
    password = request.json['psswd']
    DbFunct.updatePassword(password, email)
    return jsonify({'succes': 1})


@app.route('/login', methods=['POST'])
def login():
    """login route to the application """
    # Encrypt password.
    password = hashlib.sha224(escape(request.form['password'])).hexdigest()
    user = DbFunct.recupUtilisateur(escape(request.form['email']), password)
    if user is None:
        return redirect(url_for('page_authent'))
    else:
        session['pseudo'] = user['pseudo']
        session['email'] = user['email']
        session['password'] = user['password']
        session['playlist'] = []
        return redirect(url_for('accueil'))


# Music Pages and APIs


@app.route('/accueil', methods=['GET'])
def accueil():
    """Main route that makes call to the recupMusic function and return the home page if the email is in the session    """
    if 'pseudo' in session:
        # Get a playlist from DB if client does NOT has one.
        if not session['playlist']:
            for music in DbFunct.listeMusiqueYoutube():
                session['playlist'].append(
                    json.dumps(music.nomArtist + " - " + music.nomAlbum + " - " + music.titre).replace('"', ""))

        liste = session['playlist']
        print "accueil liste: {liste}".format(liste=liste)

        # TODO seems to be broken.. Get the first song from the list, or from the request arguments.
        if (request.args.get('compositeur') or request.args.get('titre')) is None:
            music = DbFunct.recupMusiqueYoutube(liste[0].split(" - ")[0], liste[0].split(" - ")[1],
                                                liste[0].split(" - ")[2])
        else:
            music = DbFunct.recupMusiqueYoutube(request.args.get('compositeur'), request.args.get('album'),
                                                request.args.get('titre'))

        return render_template('accueil.html', music=music, musiqueliste=liste, pseudo=session['pseudo'])

    else:
        return redirect(url_for('page_authent'))


@app.route('/accueil', methods=['POST'])
def chercher():
    """route to get the Home page of the application in case where a mood is set by the user """
    if 'pseudo' in session:
        # Check if there was any search.
        if request.form['search'] is not None:
            recherche = escape(request.form['search']).encode("utf-8")
            print recherche

            listeMotCle = recherche.split()
            session['playlist'] = []

            # Check if search was empty, redirect to home.
            if not listeMotCle:
                return redirect("/accueil")

            # Search music by arguments, or by a Mood (set by the same user).
            if (listeMotCle[0] != "humeur:"):
                listMusic = DbFunct.chercherMusiqueYoutube(listeMotCle)
            else:
                listMusic = DbFunct.algoMatchYoutube(listeMotCle[1:], session['email'])

            # Cerate playlist.
            for music in listMusic:
                session['playlist'].append(
                    json.dumps(music.nomArtist + " - " + music.nomAlbum + " - " + music.titre).replace('"', ""))
                print session['playlist']

            # Get music from the playlist and the DB
            listeMusiques = session['playlist']
            if not listeMusiques:
                return redirect("/accueil")
            else:
                music = None
                # (Not used)
                music = DbFunct.recupMusiqueYoutube(listeMusiques[0].split(" - ")[0], listeMusiques[0].split(" - ")[1],
                                                    listeMusiques[0].split(" - ")[2])
                return render_template('accueil.html', music=music, musiqueliste=listeMusiques,
                                       pseudo=session['pseudo'])
        else:
            return redirect("/accueil")
    else:
        return redirect(url_for('page_authent'))


@app.route('/top_music')
def top_music():
    """Route to Get the list of Top Music for a user according to the email , return top.html page"""
    email = session['email']
    liste = DbFunct.listTopMusicAll()
    return render_template('top.html', list_music=liste, pseudo=session['pseudo'])


@app.route('/last_music')
def last_music():
    """Route to Get the last music list, return last.html"""
    liste = DbFunct.lastMusic()
    return render_template('last.html', list_music=liste, pseudo=session['pseudo'])


@app.route('/api/getMusic', methods=['GET'])
def getMusic():
    """API getMusic route makes a GET to get the Music from the DB"""
    if not request.json:
        abort(300)
    music = DbFunct.recupMusiqueYoutube(request.json['music'].split(" - ")[0], request.json['music'].split(" - ")[1],
                                        request.json['music'].split(" - ")[2])
    return jsonify({'Artist': music.nomArtist, 'Album': music.nomAlbum, 'Titre': music.titre, 'Annee': music.Annee,
                    'Label': music.Label, 'musicPath': music.musicPath, 'imagePath': music.imagePath})


@app.route('/api/note', methods=['POST'])
def rating():
    """API note to set a note for a song """
    if not request.json:
        abort(300)
    email = session['email']
    music = DbFunct.recupMusique(request.json['music'].split("-")[0], request.json['music'].split("-")[1],
                                 request.json['music'].split("-")[2])
    note = request.json['note']
    DbFunct.insererNote(email, music, note)
    return jsonify({'succes': 1})


@app.route('/logout')
def logout():
    """route to logout from the application """
    session.clear()
    return redirect(url_for('page_authent'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """ route to the user profile """
    liste = []
    liste = DbFunct.listTopMusicUser(session['email'])
    img = []
    img = DbFunct.getUserImage(session['email'])
    print img
    if request.method == 'GET':
        return render_template('profil.html', email=session['email'], pseudo=session['pseudo'], list_music=liste,
                               image=img[0])

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1]
        filename = session['email'] + '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = app.config['UPLOAD_FOLDER'].split(".")[1] + '/' + filename
        DbFunct.updateUserImage(filename, session['email'])
        return render_template('profil.html', email=session['email'], pseudo=session['pseudo'], list_music=liste,
                               image=filename)


@app.route('/api/humeur', methods=['POST'])
def setHumeur():
    """route to post a mood to song """
    if not request.json:
        abort(300)
    email = session['email']
    music = DbFunct.recupMusique(request.json['music'].split("-")[0], request.json['music'].split("-")[1],
                                 request.json['music'].split("-")[2])
    humeur = request.json['humeur']
    DbFunct.insererHumeur(email, music, humeur)
    return jsonify({'succes': 1})


if __name__ == '__main__':
    app.run(debug=True, ssl_context=context)
