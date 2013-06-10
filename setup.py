from distutils.core import setup

setup(name='academic-cv-writer',
      version='1.0',
      py_modules=['cv-writer']
      requires=['PyYAML (>=3.01)', 'Jinja2', 'pybtex (>=0.16)']
      )