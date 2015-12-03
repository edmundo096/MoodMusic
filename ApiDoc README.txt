# Installation (Requires node.js)
npm install apidoc -g

# Execution (to generate doc):
1. Move into the project's root directory.
2. Run:
    apidoc -i . -o static/apidoc/ -f "(DbFunct|server).py" -t static/apidoc-template/

# Template Info
Based on the Default template of apiDoc v0.13.1, but whit a fix for GET in AJAX.
