from setuptools import setup
import sokery

setup(
  name = 'sokery',
  packages = ['sokery', 'sokery.web'],  
  version = sokery.__version__,
  description = 'Socket testing with web interface',
  install_requires=['tornado'],
  package_data = {'sokery': ['web/views/index.html']},
  author = 'Gamaliel Espinoza',
  author_email = 'gamaliel.espinoza@gmail.com',
  url = 'https://github.com/gamikun/sokery',
  keywords = ['sokery'], 
  classifiers = [],
)
