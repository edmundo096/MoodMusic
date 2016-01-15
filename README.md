
# MusicMood

*Note*: the commands listed here where used on a Windows system. May differ for Unix systems.


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

### APIdoc (Requires node.js)

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