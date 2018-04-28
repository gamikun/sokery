import tornado.web
import socket
import json
from datetime import datetime
from tcp import TCPServer
import logging
import os


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.servers = {}

    @property
    def report_clients(self):
        return self.settings['report_clients']

    @property
    def listen_to(self):
        return self.settings['listen_to']

    def listen(self, port):
        super(Application, self).listen(port)
        
        # If there are preconfigured ports, just
        # open them from with "open_port" function.
        ports = self.listen_to
        if isinstance(ports, list):
            for port in ports:
                self.open_port(port)

    def open_port(self, port, options=None):
        """ Opens a port and adds it to the stack """

        try:
            server = TCPServer()
            server.report_clients = self.report_clients
            server.listen(port)

            self.servers[port] = server

            if options:
                server.echo_all = bool(options.get('echo_all', None))
                logging.info("echo all: {}".format(server.echo_all))

            self.report('success',
                msg='listening in port {}'.format(port)
            )
            self.report('new-server',
                msg={
                    'port': port,
                    'server_id': server.uuid
                }
            )

        except socket.error as ex:
            if ex.errno == 13:
                self.report('error',
                    msg='cannot open port {}'.format(port)
                )

            elif ex.errno == 48:
                self.report('error',
                    msg='port {} already in use'\
                        .format(port)
                )

            else:
                self.report('error', msg=str(ex))

        except Exception as ex:
            self.report('error', msg=str(ex))

    def close_port(self, port):
        self.servers[port].stop()
        del self.servers[port]
        self.report('stopped-server', msg={'port': port})

    def report(self, op, msg='error'):
        logging.info("{}: {}".format(op, msg))
        for client in self.report_clients:
            client.write_message(json.dumps({
                'op': op,
                'message': msg,
            }))

