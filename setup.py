from setuptools import setup
import sokery

setup(
  name = 'sokery',
  packages = ['sokery', 'sokery.web'],  
  long_description=open('README.md').read(),
  version = sokery.__version__,
  description = 'Socket testing with web interface',
  install_requires=['tornado'],
  scripts = [join(binpath, 'sokery')],
  package_data = {
    'sokery': ['web/views/index.html', 'web/views/ng.js']
  },
  author = 'Gamaliel Espinoza',
  author_email = 'gamaliel.espinoza@gmail.com',
  url = 'https://github.com/gamikun/sokery',
  keywords = ['sokery'], 
  classifiers = [],
)
