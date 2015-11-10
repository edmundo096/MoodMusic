from sqlalchemy import *
from sqlalchemy.sql import *


def init():
	engine = create_engine('mysql+pymysql://root:lokman@localhost/siteweb?charset=utf8', echo=False)
	metadata = MetaData(engine)
	connection = engine.connect()
	return connection




def insertUser(pseudo_u, email_u, password_u):
	connection = init()
	sql="INSERT INTO users set email='"+email_u.encode("utf-8")+"', password='"+password_u.encode("utf-8")+"', pseudo='"+pseudo_u.encode("utf-8")+"'"
	connection.execute(sql)

def updateUserImage(image, email):
	connection = init()
	sql = "UPDATE users SET imagePath='"+image.encode("utf-8")+"' WHERE users.email='"+email.encode("utf-8")+"'" 
	connection.execute(sql)

def getUserImage(email):
	connection = init()
	sql = "SELECT imagePath FROM users WHERE users.email='"+email.encode("utf-8")+"'"
	picture = []
	for img in connection.execute(sql):
		picture = img
	return picture

def updatePassword(password, email):
	connection = init()
	sql = "UPDATE users SET password='"+password.encode("utf-8")+"' WHERE users.email='"+email.encode("utf-8")+"'"
	connection.execute(sql)

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
	
