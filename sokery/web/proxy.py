from tornado.web import RequestHandler
from binascii import hexlify
import requests
import json
import os


class Error(Exception): pass

class ProxyRequestHandler(RequestHandler):

    sokery_methods = ['connect', 'received']

    def post(self):
        report_clients = self.settings['report_clients']
        headers = self.request.headers
        sk_method = headers.get('x-sokery-method')
        app_name = headers.get('x-sokery-app-name')
        ct = headers.get('content-type', None)
        data_recvd = self.request.body
        src_address = headers.get('x-sokery-client-address', None)
        address = src_address.split(':')

        if not app_name:
            self.write('invalid app name')
            return

        if not sk_method in self.sokery_methods:
            self.write('invalid sokery method')
            return

        if len(address) < 3:
            self.write('invalid address')
            return

        # convert ports to number
        address[1] = int(address[1])
        address[2] = int(address[2])

        if ct == 'application/octet-stream':
            # TODO: unify with tcp.py method, it's 
            #       "very" repeated.
            pkg = json.dumps({
                'op': 'recvd',
                'is_binary': False,
                'data': data_recvd,
                'from': address,
                'is_proxied': True,
                'proxy_name': app_name
            })
            for client in report_clients:
                client.write_message(pkg)

        else:
            self.write('error')


class ProxyClient(object):
    __slots__ = ['url', 'app_name']

    def __init__(self, url, app_name=None):
        self.url = url
        if not app_name:
            self.app_name = 'app{}'.format(
                hexlify(os.urandom(3))
            )
        else:
            self.app_name = app_name

    def post_recvd(self, data, address):
        if len(address) < 3:
            raise Error('expecting 3 address params')

        addr = '{}:{}:{}'.format(*address)

        headers = {
            'content-type': 'application/octet-stream',
            'x-sokery-app-name': self.app_name,
            'x-sokery-method': 'received',
            'x-sokery-client-address': addr
        }
        print(addr)
        response = requests.post(self.url,
                                 data=data,
                                 headers=headers,
                                 )
        print(response.content)


if __name__ == '__main__':
    addr = ('127.0.0.1', 12341, 4995)
    client = ProxyClient('http://127.0.0.1:4991/proxy')
    client.post_recvd('SEG1,RPT,00:01:02:03:05:1,2,3,0\n', addr)
