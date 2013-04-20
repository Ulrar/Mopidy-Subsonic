# library.py ---
# "THE BEER-WARE LICENSE" (Revision 42):
# <lemonnierk@ulrar.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
#
# Filename: library.py
# Description:
# Author: Kevin Lemonnier
#           By: Kevin Lemonnier
# Created: Wed Apr 17 19:54:44 2013 (+0200)
# Last-Updated: Sat Apr 20 22:03:24 2013 (+0200)
# Version:
#     Update #: 41

# Change Log:
#
#
#

# Code:

from __future__ import unicode_literals

import logging
import libsonic

from mopidy.backends import base
from mopidy.models import Track, SearchResult, Artist

logger = logging.getLogger('mopidy.backends.subsonic')

class SubsonicLibraryProvider(base.BaseLibraryProvider):
    def __init__(self, *args, **kwargs):
        super(SubsonicLibraryProvider, self).__init__(*args, **kwargs)

    def find_exact(self, query=None, uris=None):
        return self.search(query=query, uris=uris)

    def lookup(self, uri):
        return []

    def refresh(self, uri=None):
        self.search()

    def search(self, query=None, uris=None):
        logger.info('subsonic search %s' % query)
        if not query:
            tracks = []
            for letter in self.backend.subsonic.getArtists().get('artists').get('index'):
                for artist in letter.get('artist'):
                    if type(artist) is dict:
                        for album in self.backend.subsonic.getArtist(artist.get('id')).get('artist').get('album'):
                            if type(album) is dict:
                                for song in self.backend.subsonic.getAlbum(album.get('id')).get('album').get('song'):
                                    if type(song) is dict:
                                        tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists={Artist(name=song.get('artist'))}, album=song.get('album'), track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
            return tracks
        else:
            return []


#

#
# library.py ends here
