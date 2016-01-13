How to install flask: 
http://flask.pocoo.org/docs/0.10/installation/


Debug mode (Flask):
1. Open server.py
2. Set 'use_https' at almost the end, to False for HTTP or True for HTTPS (e.g. use_https = False).
3. Save and run on terminal/console:
$ python server.py
 for HTTP
 * Running on http://127.0.0.1/ (or http://localhost/)
 or for HTTPS
 * Running on https://127.0.0.1/ (or https://localhost/)


Normal mode (Tornado):
1. Open start_tornado.py
2. Set 'use_https' at almost the end, to False for HTTP or True for HTTPS (e.g. use_https = False).
3. Save and run on terminal/console:
$ python start_tornado.py
 for HTTP
 * Running on http://127.0.0.1/ (or http://localhost/)
 or for HTTPS
 * Running on https://127.0.0.1/ (or https://localhost/)


To freeze and dump the installed libraries from the venv with pip into 'requirements.txt':
1. cd venv\Scripts
2. python -m pip freeze > requirements.txt

To install from it in another environment:
1. python -m pip install -r requirements.txt



# APIdoc Installation (Requires node.js)
npm install apidoc -g

# Execution (to generate doc):
1. Move into the project's root directory.
2. Run:
    apidoc -i . -o static/apidoc/ -f "(DbFunct|server).py" -t static/apidoc-template/

# Template Info
Based on the Default template of apiDoc v0.13.1, but whit a fix for GET in AJAX.