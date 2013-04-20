# __init__.py ---
# "THE BEER-WARE LICENSE" (Revision 42):
# <lemonnierk@ulrar.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
#
# Filename: __init__.py
# Description:
# Author: Kevin Lemonnier
#           By: Kevin Lemonnier
# Created: Wed Apr 17 19:33:41 2013 (+0200)
# Last-Updated: Sat Apr 20 18:06:03 2013 (+0200)
# Version:
#     Update #: 14

# Change Log:
#
#
#

# Code:

from __future__ import unicode_literals

import os

import mopidy
from mopidy import config, exceptions, ext

__version__ = '0.1'

class Extension(ext.Extension):

    dist_name = 'Mopidy-Subsonic'
    ext_name = 'subsonic'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['hostname'] = config.Hostname()
        schema['port'] = config.Port()
        schema['ssl'] = config.String()
        schema['username'] = config.String()
        schema['password'] = config.Secret()
        return schema

    def validate_environment(self):
        try:
            import libsonic
        except ImportError as e:
            raise exceptions.ExtensionError('py-sonic library not found', e)

    def get_backend_classes(self):
        from .actor import SubsonicBackend
        return [SubsonicBackend]

#

#
# __init__.py ends here
