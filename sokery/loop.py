from os.path import join, dirname
from web.app import Application
from tornado.ioloop import IOLoop
from web.admin import LiveHandler,\
					  StaticFileHandler
from web.proxy import ProxyRequestHandler
from argparse import ArgumentParser


basepath = dirname(__file__)
webpath = join(basepath, 'web')
viewspath = join(webpath, 'views')
indexpath = join(viewspath, 'index.html')

urlmap = [
	(r'/live', LiveHandler, ),
	(r'/()$', StaticFileHandler, {'path': indexpath}),
]

def start_loop(port=4991, listen_to=None, proxy_http=False):
	if proxy_http:
		urlmap.append((r'/proxy', ProxyRequestHandler))

	app = Application(urlmap,
		report_clients=[],
		listen_to=listen_to,
		proxy_http=proxy_http,
		)
	app.listen(port)
	loop = IOLoop.current()
	loop.start()

if __name__ == '__main__':
	from argparse import ArgumentParser
	from utils import portlist

	parser = ArgumentParser()
	parser.add_argument('-p', dest='port', default=4991, type=int)
	parser.add_argument('-l', dest='listen', type=portlist)
	parser.add_argument('--proxy-http', action='store_const',
						const=True, default=False, dest='proxy_http')

	args = parser.parse_args()

	try:
		start_loop(port=args.port,
				   listen_to=args.listen,
				   proxy_http=args.proxy_http,
				   )
	except KeyboardInterrupt:
		print('end of loop')