from mutagen.mp3 import MP3
from dev_tools import get_file_names_in_folder
import tkinter as tk


class AudioTrack:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio = MP3(file_path)
        self.title = self.audio['TIT2'].text[0] if 'TIT2' in self.audio else None
        self.artist = self.audio['TPE1'].text[0] if 'TPE1' in self.audio else None
        self.album = self.audio['TALB'].text[0] if 'TALB' in self.audio else None
        self.album_artist = self.audio['TPE2'].text[0] if 'TPE2' in self.audio else None
        self.genre = self.audio['TCON'].text[0] if 'TCON' in self.audio else None
        self.year = self.audio['TDRC'].text[0] if 'TDRC' in self.audio else None
        self.track_number = self.audio['TRCK'].text[0] if 'TRCK' in self.audio else None


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
            return audio_track.title in self.title
        return self.title == audio_track.title

    def _check_artist(self, audio_track):
        if not self.artist:
            return True
        if self.artist_part:
            return audio_track.artist in self.artist
        return self.artist == audio_track.artist

    def _check_genre(self, audio_track):
        if not self.genre:
            return True
        if self.genre_part:
            return audio_track.genre in self.genre
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
        elif isinstance(other, AudioTrack) or isinstance(other, AudioTrackMp3):
            return self._check_title(other) and self._check_artist(other) and self._check_genre(other) and \
                (self.year_ignore or self.year_max > other.get_year_safe() > self.year_min)
        return False


class AudioTrackMp3(AudioTrack):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.file_type = 'mp3'

    def get_year_safe(self):
        try:
            y = int(str(self.year))
            return y
        except ValueError:
            return -1


class App:
    def __init__(self, master):
        self.master = master
        self.listbox = tk.Listbox(self.master, width=100, height=30)
        self.listbox.pack()

        self.button = tk.Button(self.master, text="Click me!", command=self.click_button)
        self.button.pack()

    def click_button(self):
        self.listbox.insert(tk.END, 'hello world')


folder_path = input('Please, enter path to the folder with yours mp3 files: ')
# Search all mp3 files in folder
mp3_files = get_file_names_in_folder(folder_path, 'mp3')

count_of_files = len(mp3_files)
if count_of_files != 0:
    print(f'{count_of_files} MP3 files found')
else:
    print('No MP3 files found')

audio_tracks_list = []

print('Indexing')

for mp3_file in mp3_files:
    print('...............')
    audio_tracks_list.append(AudioTrackMp3(f'{folder_path}\\{mp3_file}'))

item_index = 0

filter_mp3 = AudioTrackFilter()
filter_mp3.artist = 'Queen'

for song in audio_tracks_list:
    if filter_mp3 == song:
        print("-----------------------------------------")
        print(f"Track    № {item_index + 1}")
        print("Title:  ", song.title)
        print("Artist: ", song.artist)
        print("Genre:  ", song.genre)
        print("Album:  ", song.album)
        print("Format  ", song.file_type)
        print("Year    ", song.year)
        print("")
        item_index += 1

root = tk.Tk()
root.geometry('620x500')

app = App(root)
root.mainloop()
