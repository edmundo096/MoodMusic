from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import tornado.options
import server


tornado.options.define("port", default=80, help="run on the given port", type=int)

tornado.options.parse_command_line()


http_server = HTTPServer(WSGIContainer(server.app))
http_server.listen(tornado.options.options.port)

IOLoop.instance().start()