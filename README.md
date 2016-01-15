
# MusicMood

This project was initially made for the Dynamic Web Systems course at Luleå University of Technology.

The initial idea was, while having a collection of music from choosing from, to generate playlists 
of songs depending  from the mood or moods searched, which ones were assigned previously by each user 
(i.e. by manually text searching for songs, by searching by related genres of the current mood, or 
by a random search).

Right now, it’s possible to log in and to give the music you listen a certain kind of ’mood’.
Then, you can play music in a certain ’mood’, such as ’chill’, ’sad, ’aggressive’, and many more. 
This gives you a way to listen music and without thinking about it.

**Project page:** http://moodmusicproject.blogspot.com/


*Note*: The commands listed here where used on a Windows system. May differ for Unix systems.


## Requirements

* Python 2.7.10 (with *pip*, normally selected at python installation time. Not tested with Python 3).
* MySQL (used Community Edition v 5.6).
* For development for generating the ApiDocs: NodeJS.


## Installation

One can decide where to install this app, if globally or in a virtual environment (a.k.a. **venv**). Here we will use the **venv** way.

### Installing in a Virtual environment (venv)

1. Verify that *pip* is installed:
    * On Mac/Linux execute: `$ sudo pip install virtualenv`.
    * On Ubuntu execute: `$ sudo apt-get install python-virtualenv`.
    * On Windows execute: `easy_install pip`, and then `pip install virtualenv`.
    Otherwise check this [Flask docs: pip and distribute on Windows](http://flask.pocoo.org/docs/0.10/installation/#pip-and-distribute-on-windows).
2. Create/navigate to the project directory (i.e. MoodMusic):
    For both Windows and Mac/Linux:
    1. `cd myproject`
    2. `virtualenv venv`
3. Activate the new **venv** in the command line/terminal:
    * On Mac/Linux: `$ . venv/bin/activate`.
    * On Windows: `venv\scripts\activate`.
    You should now have the virtual environment in the console prompt.

4. Now, just install all the Python dependencies into the **venv** by using *pip*:
```
python -m pip install -r requirements.txt
```
    This should read the `requirements.txt` file located on the project root directory.

> *Note*: We can also use the guide for **venv**, from Flask docs:

> * How to install Flask: http://flask.pocoo.org/docs/0.10/installation/

### MySQL Database configuration

#### Create the Database (a.k.a *Schema*)
Having the MySQL service installed, to create the app Database do the following:

1. Open a command line/terminal window.
2. Navigate to the project root directory (i.e. MoodMusic) and execute:
    * On Unix: `mysql web_db < db_dump.sql`.
    * On windows: `mysql -u [user] -p < db_dump.sql`, otherwise `mysql -u [user] -p web_db < db_dump.sql`.
    Where *user* is your MySQL DB user.
3. If there is a password for the DB user, enter it.

If you need more help, please check this StackOverflow question: [How to import an SQL file using the command line in MySQL?](http://stackoverflow.com/questions/17666249/how-to-import-an-sql-file-using-the-command-line-in-mysql).

If you are still getting errors, execute the SQL statements inside the file manually, by opening the file and copy-pasting it, by using `mysql` commandline utility.  

#### Configure the app URL connection string
To use the app with your database, you need to set the connection string on the configuration file, by doing the following:

1. Open `config.py`, and locate the line for the `db_url` variable.
2. Change the value for `'mysql+pymysql://[user]:[password]@[host_direction]/web_db?charset=utf8'`
    Where:
    * *user*:           The MySQL user to connect as, commonly used is `root`.
    * *password*:       The MySQL user password.
    * *host_direction*: The direction of where the MySQL service is hosted and accessible. When running on the same machine, usually is `localhost`.
3. Restart the app if it was already running on Normal (Tornado) mode.

*Note*: Follow the file `config.py` comments for more information about the connection string and its structure.    


## Running

*Note*: both Flask and Tornado share the same variable, if it's set to use HTTPS, both will use it when launched respectively. 

### Debug mode (Flask):
1. Open `server.py`.
2. Set `use_https` at almost the end, to `False` for HTTP or `True` for HTTPS (e.g. `use_https = False`).
3. Save and run on terminal/console:
    `$ python server.py`
    * For **HTTP**: Running on http://127.0.0.1/ (or http://localhost/)
    * Or for **HTTPS**: Running on https://127.0.0.1/ (or https://localhost/)

### Normal mode (Tornado):
1. Open `start_tornado.py`.
2. Set `use_https` at almost the end, to `False` for HTTP or `True` for HTTPS (e.g. `use_https = False`).
3. Save and run on terminal/console:
    `$ python start_tornado.py`
    * For **HTTP**: Running on http://127.0.0.1/ (or http://localhost/)
    * Or for **HTTPS**: Running on https://127.0.0.1/ (or https://localhost/)


## For Developing

### pip Commands

To freeze and dump the installed libraries from the **venv** with *pip* into *`requirements.txt`*:

1. `cd venv\Scripts`
2. `python -m pip freeze > requirements.txt`

To install from it in another environment:

1. `python -m pip install -r requirements.txt`


### APIdoc (Requires NodeJS)

#### Installation

After having NodeJS installed, execute the following command to isntal ApiDoc globally.
```
npm install apidoc -g
```

#### Execution (to generate doc):
1. Move into the project's root directory.
2. Run:
    `apidoc -i . -o static/apidoc/ -f "(DbFunct|server).py" -t static/apidoc-template/`

##### Template Info
Based on the Default template of apiDoc v0.13.1, but whit a fix for GET in AJAX.