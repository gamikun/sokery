from os.path import join, dirname
from web.app import Application
from tornado.ioloop import IOLoop
from web.admin import LiveHandler,\
					  StaticFileHandler
from argparse import ArgumentParser


basepath = dirname(__file__)
webpath = join(basepath, 'web')
viewspath = join(webpath, 'views')
indexpath = join(viewspath, 'index.html')

urlmap = [
	(r'/live', LiveHandler, ),
	(r'/()$', StaticFileHandler, {'path': indexpath}),
]

def start_loop(port=4991, listen_to=None):
	app = Application(urlmap,
		report_clients=[],
		listen_to=listen_to,
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

	args = parser.parse_args()

	try:
		start_loop(port=args.port,
				   listen_to=args.listen
				   )
	except KeyboardInterrupt:
		print('end of loop')