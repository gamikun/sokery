from __future__ import absolute_import
from os.path import join, dirname
from sokery.web.app import Application
from tornado.ioloop import IOLoop
from sokery.web.admin import LiveHandler,\
					  StaticFileHandler
from sokery.web.proxy import ProxyRequestHandler
from argparse import ArgumentParser
import logging

logging.getLogger().setLevel(logging.INFO)

basepath = dirname(__file__)
webpath = join(basepath, 'web')
viewspath = join(webpath, 'views')
indexpath = join(viewspath, 'index.html')
angularpath = join(viewspath, 'angular.min.js')

urlmap = [
	(r'/live', LiveHandler, ),
	(r'/(.+)$', StaticFileHandler, {'path': viewspath}),
	(r'/(.*)$', StaticFileHandler, {'path': indexpath}),
]

def start_loop(port=4991, listen_to=None, proxy_http=False,
			   allowed_ports=None):
	logging.info('starting in port {}'.format(port))
	logging.info('allowed_ports {}'.format(allowed_ports))
	if proxy_http:
		urlmap.append((r'/proxy', ProxyRequestHandler))

	app = Application(urlmap,
		report_clients=[],
		listen_to=listen_to,
		proxy_http=proxy_http,
		allowed_ports=allowed_ports,
		)
	app.listen(port)
	loop = IOLoop.current()
	loop.start()

if __name__ == '__main__':
	try:
		start_loop()
	except KeyboardInterrupt:
		logging.info('bye')