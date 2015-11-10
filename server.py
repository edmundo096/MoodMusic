from flask import Flask
app = Flask(__name__)

@app.route('/')
def start():
	session['playlist']=[]
	return redirect(url_for('accueil'))

if __name__ == '__main__':
    app.run()	

