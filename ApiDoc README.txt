# Installation (Requires node.js)
npm install apidoc -g

# Execution (to generate doc):
1. Move into the project's root directory.
2. Run:
    apidoc -i . -o static/apidoc/ -f "(DbFunct|server).py"
