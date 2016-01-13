from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import tornado.options
import server
import os


tornado.options.define("port_http", default=80, help="run http on the given port", type=int)
tornado.options.define("port_https", default=443, help="run https on the given port", type=int)

tornado.options.parse_command_line()

appPath = os.path.dirname(os.path.realpath(__file__))


use_https = False

if __name__ == '__main__':
    if use_https:
        http_server = HTTPServer(WSGIContainer(server.app), ssl_options={
            "certfile": appPath + '/ssl.crt',
            "keyfile": appPath + '/ssl.key'
        })
        http_server.listen(tornado.options.options.port_https)
    else:
        http_server = HTTPServer(WSGIContainer(server.app))
        http_server.listen(tornado.options.options.port_http)

    IOLoop.instance().start()