import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='academic-cv-builder',
    version='0.1',
    packages=find_packages(),
    scripts=['scripts/cv-builder'],
    data_files=[('templates', ['templates/*.tex', 'templates/*.yaml'])],
    install_requires=['PyYAML>=3.01', 'Jinja2', 'pybtex>=0.16'],
)
