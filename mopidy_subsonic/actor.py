# actor.py ---
# "THE BEER-WARE LICENSE" (Revision 42):
# <lemonnierk@ulrar.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
#
# Filename: actor.py
# Description:
# Author: Kevin Lemonnier
#           By: Kevin Lemonnier
# Created: Sat Apr 20 17:58:23 2013 (+0200)
# Last-Updated: Sat Apr 20 18:09:57 2013 (+0200)
# Version:
#     Update #: 5

# Change Log:
#
#
#

# Code:

from __future__ import unicode_literals

import logging
import pykka
import libsonic

from mopidy.backends import base
from .library import SubsonicLibraryProvider

logger = logging.getLogger('mopidy.backends.subsonic')


class SubsonicBackend(pykka.ThreadingActor, base.Backend):

    def __init__(self, config, audio):
        super(SubsonicBackend, self).__init__()

        self.config = config
        self.hostname = config.get("hostname")
        self.port = config.get("port")
        self.username = config.get("username")
        self.password = config.get("password")
        if (config.get("ssl") == "yes"):
            self.hostname = 'https://' + self.hostname
        else:
            self.hostname = 'http://' + self.hostname

        self.library = SubsonicLibraryProvider(backend=self)
        self.playback = None
        self.playlists = None

        self.uri_schemes = None

        self.subsonic = libsonic.Connection(
            self.hostname,
            self.username,
            self.password,
            self.port
        )
        logger.info('Subsonic using %s:%d as server', hostname, port)

    def on_start(self):
        pass

    def on_stop(self):
        pass

#

#
# actor.py ends here
