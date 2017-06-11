from os.path import join, dirname
from tornado.web import Application
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

def start_loop():
	app = Application(urlmap, report_clients=[])
	app.listen(4991)
	loop = IOLoop.current()
	loop.start()

if __name__ == '__main__':
	start_loop()