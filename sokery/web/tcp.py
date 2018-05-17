import json
import tornado.gen
import tornado.tcpserver
from tornado.iostream import StreamClosedError
from binascii import hexlify
import os


class TCPServer(tornado.tcpserver.TCPServer):

    def __init__(self, *args, **kwargs):
        super(TCPServer, self).__init__(*args, **kwargs)
        self.report_clients = None
        self.uuid = hexlify(os.urandom(8)).decode('utf8')
        self.is_hex_digest = True

    def listen(self, port):
        self.port = port
        self.echo_all = False
        super(TCPServer, self).listen(port)

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        print('connection from {}'.format(address))

        pkg = json.dumps({
            'op': 'newclient',
            'from': address + (self.port, ),
            })

        for client in self.report_clients:
            client.write_message(pkg)

        while True:
            try:
                data = yield stream.read_bytes(4096, partial=True)
                pkg = json.dumps({
                    'op': 'recvd',
                    'is_hex_digest': self.is_hex_digest,
                    'data': hexlify(data).decode('utf8') \
                            if self.is_hex_digest \
                            else data.decode('utf8'),
                    'from': address + (self.port, )
                })

                if self.echo_all:
                    yield stream.write(data)

                for client in self.report_clients:
                    client.write_message(pkg)

            except StreamClosedError:
                host, socket = address
                pkg = json.dumps({
                    'op': 'connection_closed',
                    'from': address + (self.port, )
                })
                for client in self.report_clients:
                    client.write_message(pkg)
                break
