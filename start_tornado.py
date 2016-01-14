from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import tornado.options
import server
import os

import config

use_https = config.use_https


if use_https:
    default_port = 443
else:
    default_port = 80

tornado.options.define("port", default=default_port, help="run on the given port", type=int)

# Overwrite the port from the Heroku run from Procfile.
tornado.options.parse_command_line()

appPath = os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    if use_https:
        http_server = HTTPServer(WSGIContainer(server.app), ssl_options={
            "certfile": appPath + '/ssl.crt',
            "keyfile": appPath + '/ssl.key'
        })
    else:
        http_server = HTTPServer(WSGIContainer(server.app))

    http_server.listen(tornado.options.options.port)

    IOLoop.instance().start()