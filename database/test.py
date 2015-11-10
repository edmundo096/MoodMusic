from sqlalchemy import *
from sqlalchemy.sql import *

	engine = create_engine('mysql+pymysql://root:lokman@localhost/siteweb?charset=utf8', echo=False)
	metadata = MetaData(engine)
	connection = engine.connect()
	return connection
