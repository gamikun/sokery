import os
import json
from tornado.web import RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from tcp import TCPServer


class LiveHandler(WebSocketHandler):

    def open(self):
        clients = self.settings['report_clients']
        clients.append(self)

    def on_close(self):
        clients = self.settings['report_clients']
        clients.remove(self)

    def on_message(self, message):
        data = json.loads(message)
        op = data['op']

        if op == 'listen':
            port = data['port']

            try:
                server = TCPServer()
                server.report_clients = self.settings['report_clients']
                server.listen(port)
                print('listening: {}'.format(port))
            except Exception as ex:
                print(ex)
