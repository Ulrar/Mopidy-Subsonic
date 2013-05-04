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
# Last-Updated: Sat May  4 17:22:51 2013 (+0200)
# Version:
#     Update #: 324

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
        self.library = None

    def find_exact(self, query=None, uris=None):
        return self.search(query=query, uris=uris)

    def lookup(self, uri):
        logger.info('Subsonic: lookup of uri %s' % uri)
        if (uri.startswith("subsonic://")):
            if (uri.find("artist") != -1):
                artist = uri[uri.find("artist") + 6:]
                res = self.search(dict(artist={artist}))
                return res.tracks
            elif (uri.find("album") != -1):
                album = uri[uri.find("album") + 5:]
                res = self.search(dict(album={album}))
                return res.tracks
            else:
                tracks = []
                tid = int(urlparse.parse_qs(urlparse.urlsplit(uri[11:]).query)["id"][0])
                song = self.backend.subsonic.getSong(tid).get('song')
                artistlist = {Artist(uri="subsonic://artist=%s" % song.get('artist'), name=song.get('artist'))}
                oalbum = Album(uri="subsonic://album=%s", name=song.get('album'), artists=artistlist)
                tracks.append(Track(uri="%s:%d/%s/%s?id=%s&u=%s&p=%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'stream.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))
                return tracks
        return []


    def refresh(self, uri=None):
        logger.info("Subsonic: refreshing library")
        self.library = {}
        res = self.backend.subsonic.search2("*:*", artistCount=0, albumCount=0, songCount=1000000000).get('searchResult2')
        for song in res.get('song'):
            artistlist = {Artist(uri="subsonic://artist=%s" % song.get('artist'), name=song.get('artist'))}
            oalbum = Album(uri="subsonic://album=%s" % song.get('album'), name=song.get('album'), artists=artistlist)
            if (song.get('artist') not in self.library):
                self.library[song.get('artist')] = {}
            if (song.get('album') not in self.library[song.get('artist')]):
                self.library[song.get('artist')][song.get('album')] = []
            self.library[song.get('artist')][song.get('album')].append(Track(uri="subsonic://%s:%d/%s/%s?id=%s&u=%s&p=enc:%s&c=mopidy&v=1.8" % (self.backend.subsonic._baseUrl, self.backend.subsonic._port, self.backend.subsonic._serverPath, 'download.view', song.get('id'), self.backend.subsonic._username, self.backend.subsonic._rawPass.encode("hex")), name=song.get('title'), artists=artistlist, album=oalbum, track_no=song.get('track'), disc_no=None, date=song.get('year'), length=song.get('duration'), bitrate=song.get('bitRate')))

    def search(self, query=None, uris=None):
        if (self.library == None):
            self.refresh()
        if not query:
            tracks = []
            artists = []
            albums = []
            for artist in self.library:
                artists.append(Artist(uri="subsonic://artist=%s" % artist, name=artist))
                for album in self.library[artist]:
                    albums.append(Album(uri="subsonic://album=%s" % album, name=album, artists=artists))
                    for song in self.library[artist][album]:
                        tracks.append(song)
            return (SearchResult(uri=None, tracks=tracks, artists=artists, albums=albums))
        else:
            tracks = []
            artists = []
            albums = []
            if ("album" in query and "artist" in "query"):
                if (query["artist"][0] in self.library and query["album"][0]  in self.library[query["artist"][0]]):
                    artists.append(Artist(uri="subsonic://artist=%s" % query["artist"][0], name=query["artist"][0]))
                    albums.append(Album(uri="subsonic://album=%s" % query["album"][0], name=query["album"][0], artists=artists))
                    tracks = self.library[query["artist"][0]][query["album"][0]]
            elif ("artist" in query):
                if (query["artist"][0] in self.library):
                    artists.append(Artist(uri="subsonic://artist=%s" % query["artist"][0], name=query["artist"][0]))
                    for album in self.library[query["artist"][0]]:
                        albums.append(Album(uri="subsonic://album=%s" % album, name=album, artists=artists))
                        for song in self.library[query["artist"][0]][album]:
                            tracks.append(song)
            elif ("album" in query):
                for artist in self.library:
                    if (query["album"][0] in artist):
                        artists.append(artists.append(Artist(uri="subsonic://artist=%s" % artist, name=artist)))
                        for song in library[artist][query["album"][0]]:
                            tracks.append(song)
                albums.append(Album(uri="subsonic://album=%s" % query["album"][0], name=query["album"][0], artists=artists))
            res = SearchResult(uri=None, tracks=tracks, artists=artists, albums=albums)
            return (res)

#

#
# library.py ends here
