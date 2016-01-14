
# Here are the variables used in the application.

# If use HTTPS instead HTTP, used by Flask and Tornado.
# Default: False
use_https = False

# The URL connection string to connect to the MySQL DB server.
# Default structure: 'mysql+pymysql://user:password@hostdirection/databasename?charset=utf8'
# where the values:
#   user:           The MySQL user to connect as, commonly used is 'root'.
#   password:       The MySQL user password.
#   hostdirection:  The direction of where the MySQL service is hosted and accessible.
#                   When running on the same machine, usually is 'localhost'.
#   databasename:   The database (or Scheme) name of the database created for the app on the MySQL service.
# Original development value: 'mysql+pymysql://root:lok@localhost/web_db?charset=utf8'
db_url = 'mysql+pymysql://root:lok@localhost/web_db?charset=utf8'

# The number of random songs to put in a playlist when the 'Get Random playlist' button is used.
# Default: 10
random_songs_number = 10