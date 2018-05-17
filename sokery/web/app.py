from __future__ import absolute_import
import tornado.web
import socket
import json
from datetime import datetime
from sokery.web.tcp import TCPServer
from sokery.utils.types import portrange
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
            if not self.is_port_allowed(port):
                raise Exception('not allowed port')
            
            server = TCPServer()
            server.report_clients = self.report_clients
            server.listen(port)

            self.servers[port] = server

            if options:
                server.echo_all = bool(options.get('echo_all', None))
                server.is_hex_digest = bool(options.get('is_binary', None))
                logging.info("echo all: {}".format(server.echo_all))

            self.report('success',
                msg='listening in port {}'.format(port)
            )
            self.report('new-server',
                msg={
                    'port': port,
                    'server_id': server.uuid,
                    'is_hex_digest': server.is_hex_digest,
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

    def is_port_allowed(self, port):
        allow_map = self.settings['allowed_ports']
        
        if not allow_map:
            return True

        for item in allow_map:
            if isinstance(item, int):
                if item == port:
                    return True
            elif isinstance(item, tuple):
                low, high = item
                if port >= low and port <= high:
                    return True

        return False

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

