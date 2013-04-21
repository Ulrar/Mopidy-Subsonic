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
# Last-Updated: Sun Apr 21 22:55:37 2013 (+0200)
# Version:
#     Update #: 252

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
        self.ltracks = None
        self.lartists = None
        self.lalbums = None

    def find_exact(self, query=None, uris=None):
        return self.search(query=query, uris=uris)

    def lookup(self, uri):
        logger.info('Subsonic: lookup of uri %s' % uri)
        if (uri.startswhith("subsonic:")):
            if (uri.find("artist") != -1):
                artist = uri[uri.find("artist") + 6:]
                res = self.search(dict(artist={artist}))
                return res.tracks
            elif (uri.find("album") != -1):
                album = uri[uri.find("album") + 5:]
                res = self.search(dict(album={album}))
                return res.tracks
            else:
                return []
        else:
            tracks = []
            tid = urlparse.parse_qs(urlparse.urlsplit(uri).query)[0]
            track = self.backend.subsonic.getSong(tid).get('song')
            artistlist = {Artist(uri="subsonic:artist=%s" % song.get('artist'), name=song.get('artist'))}
            oalbum = Album(uri="subsonic:album=%s", name=song.get('album'), artists=artistlist)
            tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'stream.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
            return tracks


    def refresh(self, uri=None):
        logger.info("Subsonic: refreshing library")
        (self.ltracks, self.lartists, self.lalbums) = self.getAllTracks()

    def search(self, query=None, uris=None):
        if (self.ltracks == None or self.lartists == None or self.lalbums == None):
            self.refresh()
        if not query:
            return (SearchResult(uri=None, tracks=self.ltracks[:], artists=self.lartists[:], albums=self.lalbums[:]))
        else:
            tracks = self.ltracks[:]
            artists = []
            albums = []
            for track in tracks[:]:
                if ("album" in query):
                    if not (track.album.name == query["album"][0]):
                        tracks.remove(track)
                        continue
                if ("artist" in query):
                    remove = True
                    for art in track.artists:
                        if (art.name == query["artist"][0]):
                            remove = False
                    if (remove == True):
                        tracks.remove(track)
                        continue
#                if ("date" in query):
#                    if not (track.date == query["date"][0]):
#                        tracks.remove(track)
#                        continue
                if (track.album not in albums):
                    albums.append(track.album)
                for artist in track.artists:
                    if (artist not in artists):
                        artists.append(artist)
            res = SearchResult(uri=None, tracks=tracks, artists=artists, albums=albums)
            return (res)

    def getAllTracks(self):
        tracks = []
        artists = []
        albums = []
        res = self.backend.subsonic.search2("*:*", artistCount=0, albumCount=0, songCount=1000000000).get('searchResult2')
        for song in res.get('song'):
            artistlist = {Artist(uri="subsonic:artist=%s" % song.get('artist'), name=song.get('artist'))}
            oalbum = Album(uri="subsonic:album=%s" % song.get('album'), name=song.get('album'), artists=artistlist)
            tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
            artists.append(Artist(uri="subsonic:artist=%s" % song.get('artist'), name=song.get('artist')))
            albums.append(oalbum)
        return (tracks, artists, albums)


#

#
# library.py ends here
