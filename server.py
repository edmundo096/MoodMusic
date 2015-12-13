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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# ========================================
# NAVIGATION
# ========================================

@app.route('/')
def nav_root_to_home():
    """  starting route """
    session['playlist'] = []
    return redirect(url_for('nav_home'))


@app.route('/api', methods=['GET'])
def nav_apidoc():
    return render_template('api.html', username=session['username'])

# ----------------------------------------
# User handling
# ----------------------------------------

@app.route('/register', methods=['GET'])
def nav_register():
    """Get the Registration page """
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def nav_register_post():
    """Route to Post the user Information in the DB (making call to the user_user_insert function ) and redirect to the authentication page"""
    first_name = escape(request.form['username'])
    email = escape(request.form['email'])
    password = escape(request.form['password'])
    # Encrypt password.
    password = hashlib.sha224(password).hexdigest()
    user = DbFunct.user_user_get(email, None)
    if user is None:
        DbFunct.user_user_insert(first_name, email, password)
        return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/submit_password', methods=['POST'])
def submit_password():
    """route to submit the new password   """
    if not request.json:
        abort(300)
    email = session['email']
    password = request.json['psswd']
    # TODO hashing
    DbFunct.user_password_update(password, email)
    return jsonify({'succes': 1})


@app.route('/login')
def nav_login():
    """authentication route for all users """
    if 'username' in session:
        return redirect(url_for('nav_home'))
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def nav_login_post():
    """login route to the application """
    # Encrypt password.
    password = hashlib.sha224(escape(request.form['password'])).hexdigest()
    user = DbFunct.user_user_get(escape(request.form['email']), password)
    if user is None:
        return redirect(url_for('nav_login'))
    else:
        session['username'] = user['username']
        session['email'] = user['email']
        session['password'] = user['password']
        session['playlist'] = []
        return redirect(url_for('nav_home'))


@app.route('/logout')
def logout():
    """route to logout from the application """
    session.clear()
    return redirect(url_for('nav_login'))


@app.route('/profile', methods=['GET', 'POST'])
def nav_profile():
    """ route to the user profile """
    list = []
    list = DbFunct.listTopMusicUser(session['email'])

    img = DbFunct.user_image_get(session['email'])
    print img

    # GET
    if request.method == 'GET':
        return render_template('profile.html', email=session['email'], username=session['username'], list_music=list,
                               image=img)
    # POST
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1]
        filename = session['email'] + '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = app.config['UPLOAD_FOLDER'].split(".")[1] + '/' + filename

        DbFunct.user_image_update(filename, session['email'])

        return render_template('profile.html', email=session['email'], username=session['username'], list_music=list,
                               image=filename)



# ---------------------------------------
# Music Pages
# ----------------------------------------

@app.route('/home', methods=['GET'])
def nav_home():
    """Main route that makes call to the recupMusic function and return the home page if the email is in the session    """
    if 'username' in session:
        # Get a playlist from DB if client does NOT has one.
        if not session['playlist']:
            for music in DbFunct.listMusicYoutube():
                session['playlist'].append({'artist': music.artist , 'album': music.album, 'title': music.title})

        list = session['playlist']
        print "home list: {list}".format(list=list)

        # TODO seems to be broken.. Get the first song from the list, or from the request arguments.
        if (request.args.get('artist') or request.args.get('title')) is None:
            music = DbFunct.get_song_data(list[0]['artist'], list[0]['album'],
                                          list[0]['title'])
        else:
            music = DbFunct.get_song_data(request.args.get('artist'), request.args.get('album'),
                                          request.args.get('title'))

        return render_template('home.html', music=music, music_list=list, username=session['username'])

    else:
        return redirect(url_for('nav_login'))


@app.route('/home', methods=['POST'])
def nav_home_search():
    """route to get the Home page of the application in case where a mood is set by the user """
    if 'username' in session:
        # Check if there was any search.
        if request.form['search'] is not None:
            search = escape(request.form['search']).encode("utf-8")
            print search

            listKeyword = search.split()
            session['playlist'] = []

            # Check if search was empty, redirect to home.
            if not listKeyword:
                return redirect("/home")

            # Search music by arguments, or by a Mood (set by the same user).
            if (listKeyword[0] != "mood:"):
                listMusic = DbFunct.searchMusicYoutube(listKeyword)
            else:
                listMusic = DbFunct.algoMatchYoutube(listKeyword[1:], session['email'])

            # Cerate playlist.
            for music in listMusic:
                session['playlist'].append({'artist': music.artist , 'album': music.album, 'title': music.title})
            print "home POST - session['playlist']: "
            print session['playlist']

            # Get the 1 st song from the DB for the client "music" variable (for metadata and src load).
            listMusic = session['playlist']
            if not listMusic:
                return redirect("/home")
            else:
                music = DbFunct.get_song_data(listMusic[0]['artist'], listMusic[0]['album'],
                                              listMusic[0]['title'])
                return render_template('home.html', music=music, music_list=listMusic,
                                       username=session['username'])
        else:
            return redirect("/home")
    else:
        return redirect(url_for('nav_login'))


@app.route('/top_music')
def top_music():
    """Route to Get the list of Top Music for a user according to the email , return top.html page"""
    email = session['email']
    list = DbFunct.listTopMusicAll()
    return render_template('top.html', list_music=list, username=session['username'])


@app.route('/last_music')
def last_music():
    """Route to Get the last music list, return last.html"""
    list = DbFunct.lastMusic()
    return render_template('last.html', list_music=list, username=session['username'])


# ========================================
# AJAX API
# ========================================

@app.route('/api/getMusic', methods=['GET'])
def getMusic():
    """
    @api {get} /api/getMusic Get song data
    @apiGroup Song

    @apiParam {string} artist The exact song's artist name on the system.
    @apiParam {string} album The exact song's album name on the system.
    @apiParam {string} title The exact song's title on the system.

    @apiDescription
    API getMusic route makes a GET to get the Music from the DB,
    Returns JSON object.
    """
    #@apiParam {String="info","id"} [method=id]  Especifies the information used to query the song, either with id or info.

    if  request.args.get('artist') == None or request.args.get('album') == None or request.args.get('title') == None:
        return jsonify({})

    music = DbFunct.get_song_data(request.args.get('artist'), request.args.get('album'), request.args.get('title'))
    print "api getMusic() music: "
    print music
    return jsonify({'artist': music.artist, 'album': music.album, 'title': music.title, 'year': music.year,
                    'label': music.label, 'music_path': music.musicPath, 'image_path': music.imagePath})


@app.route('/api/note', methods=['POST'])
def rating():
    """
    @api {post} /api/note Post a song rate
    @apiGroup Song

    @apiParam {string} artist The exact song's artist name on the system.
    @apiParam {string} album The exact song's album name on the system.
    @apiParam {string} title The exact song's title on the system.
    @apiParam {number{1}=1,2,3,4,5} rating The rating given to the song.
    @apiParam {string} email TODO, The email of the user that post the rating.

    @apiDescription
    API note to set a note for a song.
    Returns JSON object.
    """
    if request.json['artist'] == None or request.json['album'] == None or request.json['title'] == None or request.json['rating'] == None:
        return jsonify({'result': 0})

    if not request.json:
        abort(300)
    email = session['email']
    music = DbFunct.get_song_data(request.json['artist'], request.json['album'], request.json['title'])
    rating = request.json['rating']

    # TODO, fails if the music/song was not found (= None).
    DbFunct.insertRating(email, music, rating)
    return jsonify({'succes': 1})


@app.route('/api/humeur', methods=['POST'])
def setHumeur():
    """
    @api {post} /api/humeur Post song mood
    @apiGroup Song

    @apiParam {string} artist The exact song's artist name on the system.
    @apiParam {string} album The exact song's album name on the system.
    @apiParam {string} title The exact song's title on the system.
    @apiParam {string} mood The mood classification given to the song.
                            TODO, enumerate the moods.
    @apiParam {string} email TODO, The email of the user that post the mood classfication.

    @apiDescription
    Route to post a mood to song.
    """
    if request.json['artist'] == None or request.json['album'] == None or request.json['title'] == None or request.json['mood'] == None:
        return jsonify({'result': 0})

    if not request.json:
        abort(300)
    email = session['email']
    music = DbFunct.get_song_data(request.json['artist'], request.json['album'], request.json['title'])
    mood = request.json['mood']

    # TODO, fails if the music/song was not found (= None).
    DbFunct.insertMood(email, music, mood)
    return jsonify({'succes': 1})


# Enable HTTPS
import ssl

appPath = os.path.dirname(os.path.realpath(__file__))
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(appPath + '/ssl.crt', appPath + '/ssl.key')


if __name__ == '__main__':
    #app.run(debug=True, ssl_context=context, port=443)
    app.run(debug=True, port=80)
