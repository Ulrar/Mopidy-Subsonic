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
# Last-Updated: Sat May  4 18:28:24 2013 (+0200)
# Version:
#     Update #: 29

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
from mopidy.models import Track

logger = logging.getLogger('mopidy.backends.subsonic')


class SubsonicBackend(pykka.ThreadingActor, base.Backend):

    def __init__(self, config, audio):
        super(SubsonicBackend, self).__init__()

        self.config = config['subsonic']
        self.hostname = self.config.get("hostname")
        self.port = self.config.get("port")
        self.username = self.config.get("username")
        self.password = self.config.get("password")
        if (self.config.get("ssl") == "yes"):
            self.hostname = 'https://' + self.hostname
        else:
            self.hostname = 'http://' + self.hostname

        self.library = SubsonicLibraryProvider(backend=self)
        self.playback = SubsonicPlaybackProvider(backend=self, audio=audio)
        self.playlists = None

        self.uri_schemes = ['subsonic']

        self.subsonic = libsonic.Connection(
            self.hostname,
            self.username,
            self.password,
            self.port
        )
        logger.info('Subsonic using %s:%d as server', self.hostname, self.port)

    def on_start(self):
        self.library.refresh()

    def on_stop(self):
        pass

class SubsonicPlaybackProvider(base.BasePlaybackProvider):
    def play(self, track):
        logger.info('Getting info for track %s with name %s' % (track.uri, track.name))
        ntrack = Track(uri=track.uri[11:], name=track.name, artists=track.artists, album=track.album, track_no=track.track_no, disc_no=track.disc_no, date=track.date, length=track.length, bitrate=track.bitrate, musicbrainz_id=track.musicbrainz_id)
        return super(SubsonicPlaybackProvider, self).play(ntrack)

#

#
# actor.py ends here
