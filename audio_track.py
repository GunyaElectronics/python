from mutagen.mp3 import MP3
from dev_tools import get_file_names_in_folder


class AudioTrack:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = 'mp3'
        self.audio = MP3(file_path)
        self.title = self.audio['TIT2'].text[0] if 'TIT2' in self.audio else None
        self.artist = self.audio['TPE1'].text[0] if 'TPE1' in self.audio else None
        self.album = self.audio['TALB'].text[0] if 'TALB' in self.audio else None
        self.album_artist = self.audio['TPE2'].text[0] if 'TPE2' in self.audio else None
        self.genre = self.audio['TCON'].text[0] if 'TCON' in self.audio else None
        self.year = self.audio['TDRC'].text[0] if 'TDRC' in self.audio else None
        self.track_number = self.audio['TRCK'].text[0] if 'TRCK' in self.audio else None

    def get_year_safe(self):
        try:
            y = int(str(self.year))
            return y
        except ValueError:
            return None


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
    audio_tracks_list.append(AudioTrack(f'{folder_path}\\{mp3_file}'))

item_index = 0

for song in audio_tracks_list:
    year = song.get_year_safe()
    if year and year < 1990 and song.genre == 'Rock':
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

