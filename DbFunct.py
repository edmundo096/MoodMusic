from sqlalchemy import *
from sqlalchemy.sql import *


def init():
	engine = create_engine('mysql+pymysql://root:lok@localhost/web_db?charset=utf8', echo=False)
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


	

