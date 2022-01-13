import sys
from setuptools import setup, find_packages

with open('README.md') as readme:
    description = readme.read()

version = '0.0.1'
deps = []

setup(
    name='sockgen',
    version=version,
    url='http://pypi.python.org/pypi/sockgen/',
    author='Riza Kaan Ucak',
    author_email='rzakaan@gmail.com',
    description=('Turn (almost) any command line program into a full GUI '
                 'application with one line'),
    license='MIT',
    packages=find_packages(),
    install_requires=deps,
    include_package_data=True,
    classifiers = [
        'License :: MIT License'
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Desktop Environment',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Widget Sets',
        'Programming Language :: Python :: 3',
    ],
    long_description=description
)
