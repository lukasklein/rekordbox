from lxml import etree
import sys


class Rekordbox(object):
    def __init__(self, playlist_file):
        self.f = open(playlist_file)
        self.load_tree()
        self.load_tracks()
        self.load_playlists()

    def load_tree(self):
        self.tree = etree.parse(self.f)
        self.root = self.tree.getroot()

    def load_tracks(self):
        self.tracks = {}
        for track in list(self.root[1]):
            self.tracks[track.get('TrackID')] = {
                'name': track.get('Name', '').encode('utf-8'),
                'artist': track.get('Artist', '').encode('utf-8'),
            }

    def load_playlists(self):
        self.playlists = {}
        for playlist in list(self.root[2][0]):
            self.playlists[playlist.get('Name')] = [
                self.tracks[track.get('Key')]
                for track in list(playlist)]

    def prettyprint_playlists(self):
        for playlist in self.playlists:
            print '=' * 80
            print playlist
            print '=' * 80
            print
            for track in self.playlists[playlist]:
                print '%s - %s' % (track['name'], track['artist'])
            print


if __name__ == '__main__':
    plist = sys.argv[1]
    r = Rekordbox(plist)
    r.prettyprint_playlists()
