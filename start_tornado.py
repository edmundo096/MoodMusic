from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import server

http_server = HTTPServer(WSGIContainer(server.app))
http_server.listen(80)
IOLoop.instance().start()