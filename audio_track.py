from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import operator


class PlaylistItem:
    def __init__(self, track, is_added=False):
        self.track = track
        self.list_index = None

    def __repr__(self):
        return f"PlaylistItem({self.track.title}, {self.track.artist}, {self.track.album}, {self.track.album_artist}," \
               f" {self.track.genre})"


class AudioTrack:
    def __init__(self):
        self.title = None
        self.artist = None
        self.album = None
        self.album_artist = None
        self.genre = None
        self.year = None
        self.track_number = None
        self.is_have_cover_art = False
        self.cover_art = None

    def get_year_safe(self):
        try:
            y = int(str(self.year))
            return y
        except ValueError:
            return -1

    def is_have_cover_img(self):
        return self.is_have_cover_art

    def __repr__(self):
        return f"AudioTrack({self.title}, {self.artist}, {self.album}, {self.album_artist}, {self.genre})"


class AudioTrackFilter:
    def __init__(self):
        self.title = None
        self.title_part = True
        self.artist = None
        self.artist_part = True
        self.genre = None
        self.genre_part = True
        self.year_ignore = True
        self.year_min = 0
        self.year_max = 3000

    def _check_title(self, audio_track):
        if not self.title:
            return True
        if self.title_part:
            return self.title in audio_track.title
        return self.title == audio_track.title

    def _check_artist(self, audio_track):
        if not self.artist:
            return True
        if self.artist_part:
            return self.artist in audio_track.artist
        return self.artist == audio_track.artist

    def _check_genre(self, audio_track):
        if not self.genre:
            return True
        if self.genre_part:
            return self.genre in audio_track.genre
        return self.genre == audio_track.genre

    def __eq__(self, other):
        if isinstance(other, AudioTrackFilter):
            return (not self.title or self.title == other.title) and \
                (not self.title_part or self.title_part == other.title_part) and \
                (not self.artist or self.artist == other.artist) and \
                (not self.artist_part or self.artist_part == other.artist_part) and \
                (not self.genre or self.genre == other.genre) and \
                (not self.year_min or self.year_min == other.year_min) and \
                (not self.year_max or self.year_max == other.year_max)
        else:  # isinstance(other, AudioTrack) or isinstance(other, AudioTrackMp3) or isinstance(other, AudioTrackFlac):
            return self._check_title(other) and self._check_artist(other) and self._check_genre(other) and \
                (self.year_ignore or self.year_max > other.get_year_safe() > self.year_min)


class AudioTrackFlac(AudioTrack):
    def __init__(self, file_path):
        super().__init__()
        self.file_type = 'flac'
        self.file_path = file_path
        self.audio = FLAC(file_path)
        self.title = self.audio['TITLE'][0] if 'TITLE' in self.audio else ''
        self.artist = self.audio['ARTIST'][0] if 'ARTIST' in self.audio else ''
        self.album = self.audio['ALBUM'][0] if 'ALBUM' in self.audio else ''
        self.genre = self.audio['GENRE'][0] if 'GENRE' in self.audio else ''
        self.year = self.audio['DATE'][0] if 'DATE' in self.audio else None


class AudioTrackMp3(AudioTrack):
    def __init__(self, file_path):
        super().__init__()
        self.file_type = 'mp3'
        self.file_path = file_path
        self.audio = MP3(file_path)
        self.title = self.audio['TIT2'].text[0] if 'TIT2' in self.audio else ''
        self.artist = self.audio['TPE1'].text[0] if 'TPE1' in self.audio else ''
        self.album = self.audio['TALB'].text[0] if 'TALB' in self.audio else ''
        self.album_artist = self.audio['TPE2'].text[0] if 'TPE2' in self.audio else ''
        self.genre = self.audio['TCON'].text[0] if 'TCON' in self.audio else ''
        self.year = self.audio['TDRC'].text[0] if 'TDRC' in self.audio else None
        self.track_number = self.audio['TRCK'].text[0] if 'TRCK' in self.audio else None
        self.cover_art = self._read_cover_art()
        self.is_have_cover_art = False if self.cover_art is None else True

    def _read_cover_art(self):
        try:
            data = self.audio['APIC:'].data
        except KeyError:
            for key in self.audio.keys():
                if 'APIC' in key:
                    return self.audio[key].data
            data = None
        return data


def sort_audio_tracks_list(songs_list, sort_by):
    return sorted(songs_list, key=operator.attrgetter(sort_by))
