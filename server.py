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



@app.route('/authent')
def page_authent():
	if 'email' in session:
		return redirect(url_for('accueil'))
	else:
		return render_template('authent.html')

@app.route('/accueil', methods=['GET'])
def accueil():
		return redirect(url_for('page_authent'))

@app.route('/accueil', methods=['POST'])
def chercher():
	

		return redirect(url_for('page_authent'))

		
		
		

if __name__ == '__main__':
  app.run(debug=True) 
