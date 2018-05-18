from setuptools import setup
import sokery
import os

basepath = os.path.dirname(__file__)
binpath = os.path.join(basepath, 'bin')

setup(
  name = 'sokery',
  packages = ['sokery', 'sokery.web', 'sokery.utils'],  
  long_description=open(os.path.join(basepath, 'README.md')).read(),
  version = sokery.__version__,
  description = 'Socket testing with web interface',
  install_requires=['tornado'],
  scripts = [os.path.join(binpath, 'sokery')],
  package_data = {
    'sokery': ['web/views/index.html', 'web/views/ng.js']
  },
  author = 'Gamaliel Espinoza',
  author_email = 'gamaliel.espinoza@gmail.com',
  url = 'https://github.com/gamikun/sokery',
  keywords = ['sokery'], 
  classifiers = [],
)
