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
# Last-Updated: Sun Apr 21 00:10:09 2013 (+0200)
# Version:
#     Update #: 79

# Change Log:
#
#
#

# Code:

from __future__ import unicode_literals

import logging
import libsonic
import urlparse
import string

from mopidy.backends import base
from mopidy.models import Track, SearchResult, Artist, Album

logger = logging.getLogger('mopidy.backends.subsonic')

class SubsonicLibraryProvider(base.BaseLibraryProvider):
    def __init__(self, *args, **kwargs):
        super(SubsonicLibraryProvider, self).__init__(*args, **kwargs)

    def find_exact(self, query=None, uris=None):
        return self.search(query=query, uris=uris)

    def lookup(self, uri):
        if (uri == "/"):
            logger.info('subsonic lookup of all tracks')
            return (self.getAllTracks()[0])
        else:
            tid = urlparse.parse_qs(urlparse.urlsplit(uri).query)[0]
            logger.info('subsonic lookup of id %d' % tid)

    def refresh(self, uri=None):
        self.search()

    def search(self, query=None, uris=None):
        logger.info('subsonic search %s' % query)
        if not query:
            (tracks, artists, albums) = self.getAllTracks()
            return (SearchResult(uri=None, tracks=tracks, artists=artists, albums=albums))
        else:
            return []

    def getAllTracks(self):
        tracks = []
        artists = []
        albums = []
        for letter in self.backend.subsonic.getArtists().get('artists').get('index'):
            for artist in letter.get('artist'):
                if type(artist) is dict:
                    for album in self.backend.subsonic.getArtist(artist.get('id')).get('artist').get('album'):
                        if type(album) is dict:
                            for song in self.backend.subsonic.getAlbum(album.get('id')).get('album').get('song'):
                                if type(song) is dict:
                                    if (song.get('album') is string or song.get('album') is unicode):
                                        albname = song.get('album')
                                    else:
                                        albname = "Unknown"
                                    artistlist = {Artist(uri="", name=song.get('artist'))}
                                    oalbum = Album(uri="", name=albname, artists=artistlist)
                                    tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
                                    artists.append(Artist(uri="", name=song.get('artist')))
                                    albums.append(oalbum)
        return (tracks, artists, albums)


#

#
# library.py ends here
