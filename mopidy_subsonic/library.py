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
# Last-Updated: Sat Apr 20 17:55:18 2013 (+0200)
# Version:
#     Update #: 24

# Change Log:
#
#
#

# Code:

from __future__ import unicode_literals

import logging
import libsonic

from mopidy.backends import base
from mopidy.models import Track, SearchResult

logger = logging.getLogger('mopidy.backends.subsonic')

class SubsonicLibraryProvider(base.BaseLibraryProvider):
    def __init__(self, *args, **kwargs):
        super(SubsonicLibraryProvider, self).__init__(*args, **kwargs)

    def find_exact(self, query=None, uris=None):
        return self.search(query=query, uris=uris)

    def lookup(self, uri):
        return []

    def refresh(self, uri=None):
        pass  # TODO

    def search(self, query=None, uris=None):
        if not query:
            tracks = []
            for letter in conn.getArtists().get('artists').get('index'):
                for artist in letter.get('artist'):
                    if type(artist) is dict:
                        for album in conn.getArtist(artist.get('id')).get('artist').get('album'):
                            if type(album) is dict:
                                for song in conn.getAlbum(album.get('id')).get('album').get('song'):
                                    if type(song) is dict:
                                        tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.subsonic._baseUrl, self.subsonic._port, self.subsonic._serverPath, 'download.view', song.get('id'), self.subsonic._username, self.subsonic._rawPass), name=song.get('title'), artist=artist.get('name')))
            return tracks
        else:
            return []


#

#
# library.py ends here
