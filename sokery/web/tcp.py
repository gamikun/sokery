import json
import tornado.gen
import tornado.tcpserver
from tornado.iostream import StreamClosedError


class TCPServer(tornado.tcpserver.TCPServer):

    def __init__(self, *args, **kwargs):
        super(TCPServer, self).__init__(*args, **kwargs)
        self.report_clients = None

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        print('connection from {}'.format(address))

        pkg = json.dumps({
            'op': 'newclient',
            'address': str(address),
            })

        for client in self.report_clients:
            client.write_message(pkg)

        while True:
            try:
                data = yield stream.read_bytes(4096, partial=True)
                pkg = json.dumps({
                    'op': 'recvd',
                    'is_binary': False,
                    'data': data
                })

                if self.echo_all:
                    yield stream.write(data)

                for client in self.report_clients:
                    client.write_message(pkg)

            except StreamClosedError:
                print("fuck")
                break
