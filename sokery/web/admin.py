from __future__ import absolute_import
import os
import json
from tornado.web import RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from sokery.web.tcp import TCPServer


class LiveHandler(WebSocketHandler):

    def open(self):
        clients = self.settings['report_clients']
        clients.append(self)
        self.write_message(json.dumps({
            'op': 'list-servers',
            'msg': {
                'servers': [
                    {'port': port} \
                    for port in self.application.servers
                ]
            }
        }))

    def on_close(self):
        clients = self.settings['report_clients']
        clients.remove(self)

    def on_message(self, message):
        data = json.loads(message)
        op = data['op']

        if op == 'listen':
            port = data['port']
            options = data.get('options', None)
            self.application.open_port(port, options=options)

        elif op == 'unlisten':
            port = data['port']
            self.application.close_port(port)


