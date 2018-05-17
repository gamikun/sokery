from __future__ import absolute_import
from argparse import ArgumentParser
from sokery.utils.types import portlist
from sokery.loop import start_loop

parser = ArgumentParser()
parser.add_argument('action')
parser.add_argument('-p', dest='port', default=4991, type=int)
parser.add_argument('-l', dest='listen', type=portlist)
parser.add_argument('-a', dest='allowed_ports', type=portlist)
parser.add_argument('--proxy-http', action='store_const',
					const=True, default=False, dest='proxy_http')

args = parser.parse_args()

if args.action == 'run':
	try:
		print('listening on port {}'.format(args.port))
		start_loop(port=args.port,
				   listen_to=args.listen,
				   proxy_http=args.proxy_http,
				   allowed_ports=args.allowed_ports,
				   )
	except KeyboardInterrupt:
		print('end of loop')