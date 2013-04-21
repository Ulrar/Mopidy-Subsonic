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
# Last-Updated: Sun Apr 21 17:01:59 2013 (+0200)
# Version:
#     Update #: 150

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
            tracks = []
            artists = []
            albums = []
            for q in query:
                res = self.backend.subsonic.search2("%s: %s" % (q, query[q][0]), artistCount=1000000000, albumCount=1000000000, songCount=1000000000).get('searchResult2')
                if ('song' in res):
                    if (type(res.get('song')) == list):
                        for song in res.get('song'):
                            artistlist = {Artist(uri="", name=song.get('artist'))}
                            oalbum = Album(uri="", name=song.get('album'))
                            tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
                    else:
                        artistlist = {Artist(uri="", name=res.get('song').get('artist'))}
                        oalbum = Album(uri="", name=res.get('song').get('album'))
                        tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', res.get('song').get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=res.get('song').get('title'), artists=artistlist, album=oalbum, track_no=res.get('song').get('track'), disc_no=None, date=res.get('song').get('year'), length=res.get('song').get('duration'), bitrate=res.get('song').get('bitRate')))
                if ('album' in res):
                    if (type(res.get('album')) == list):
                        for alb in res.get('album'):
                            albums.append(Album(uri="", name=alb.get('album'), artists={Artist(uri="", name=alb.get('artist'))}))
                    else:
                        albums.append(Album(uri="", name=res.get('album').get('album'), artists={Artist(uri="", name=res.get('album').get('artist'))}))
                if ('artist' in res):
                    if (type(res.get('artist')) == list):
                        for art in res.get('artist'):
                            artists.append(Artist(uri="", name=art.get('name')))
                    else:
                        artists.append(Artist(uri="", name=res.get('artist').get('name')))
            return (SearchResult(uri=None, tracks=tracks, artists=artists, albums=albums))



    def getAllTracks(self):
        tracks = []
        artists = []
        albums = []
        res = self.backend.subsonic.search2("*:*", artistCount=0, albumCount=0, songCount=1000000000).get('searchResult2')
        for song in res.get('song'):
            artistlist = {Artist(uri="", name=song.get('artist'))}
            oalbum = Album(uri="", name=song.get('album'))
            tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
            artists.append(Artist(uri="", name=song.get('artist')))
            albums.append(oalbum)
        return (tracks, artists, albums)


#

#
# library.py ends here
