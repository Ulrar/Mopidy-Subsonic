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
# Last-Updated: Sun Apr 21 16:00:29 2013 (+0200)
# Version:
#     Update #: 139

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
                    for song in res.get('song'):
                        if (song is dict):
                            artistlist = {Artist(uri="", name=song.get('artist'))}
                            oalbum = Album(uri="", name=song.get('album'))
                            tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
                if ('album' in res):
                    if (type(res.get('album')) == list):
                        for alb in res.get('album'):
                            albums.append(Album(uri="", name=alb.get('album'), artists={Artist(uri="", name=alb.get('artist'))}))
                    else:
                        albums.append(Album(uri="", name=res.get('album').get('album'), artists={Artist(uri="", name=res.get('album').get('artist'))}))
                if ('artist' in res):
                    for art in res.get('artist'):
                        if (art is dict):
                            artists.append(Artist(uri="", name=art.get('name')))
            return (SearchResult(uri=None, tracks=tracks, artists=artists, albums=albums))



    def getAllTracks(self):
        tracks = []
        artists = []
        albums = []
        res = self.backend.subsonic.search2("a* OR b* OR c* OR d* OR e* OR f* OR g* OR h* OR i* OR j* OR k* OR l* OR m* OR n* OR o* OR p* OR q* OR r* OR s* OR t* OR u* OR v* OR w* OR x* OR y* OR z* OR A* OR B* OR C* OR D* OR E* OR F* OR G* OR H* OR I* OR J* OR K* OR L* OR M* OR N* OR O* OR P* OR Q* OR R* OR S* OR T* OR U* OR V* OR W* OR X* OR Y* OR Z* OR 0* OR 1* OR 2* OR 3* OR 4* OR 5* OR 6* OR 7* OR 8* OR 9*", artistCount=0, albumCount=0, songCount=1000000000).get('searchResult2')
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
