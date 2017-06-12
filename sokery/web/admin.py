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
            options = data.get('options', None)

            try:
                server = TCPServer()

                if options:
                    server.echo_all = bool(options.get('echo_all', None))
                    print("echo all: {}".format(server.echo_all))

                server.report_clients = self.settings['report_clients']
                server.listen(port)

                msg = 'listening in port {}'.format(port)
                if server.echo_all:
                    msg += ' (echo server)'

                self.write_message(json.dumps({
                    'op': 'success',
                    'message': msg 
                    }))

            except Exception as ex:
                self.write_message(json.dumps({
                    'op': 'error',
                    'message': str(ex)
                    }))
                print(ex)

