from tornado.web import RequestHandler
import json


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
