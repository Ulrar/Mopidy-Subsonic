# setup.py ---
# "THE BEER-WARE LICENSE" (Revision 42):
# <lemonnierk@ulrar.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
#
# Filename: setup.py
# Description:
# Author: Kevin Lemonnier
#           By: Kevin Lemonnier
# Created: Sat Apr 20 15:45:58 2013 (+0200)
# Last-Updated: Sat Apr 20 16:33:34 2013 (+0200)
# Version:
#     Update #: 11

# Change Log:
#
#
#

# Code:

from __future__ import unicode_literals

import re
from setuptools import setup, find_packages


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-Subsonic',
    version=get_version('mopidy_subsonic/__init__.py'),
    url='https://github.com/Ulrar/Mopidy-Subsonic',
    license='THE BEER-WARE LICENSE',
    author='Kevin Lemonnier',
    author_email='lemonnierk@ulrar.net',
    description='Subsonic backend for mopidy',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'setuptools',
        'Mopidy',
        'py-sonic',
    ],
    entry_points={
        'mopidy.ext': [
            'subsonic = mopidy_subsonic:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)

#

#
# setup.py ends here
