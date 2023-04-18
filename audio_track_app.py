from dev_tools import get_file_names_in_folder
from audio_track_ui import *
from audio_track import *
import threading


class App:
    def __init__(self, master_ui):
        # Algorithm elements
        self.filter_metadata = AudioTrackFilter()
        self.audio_tracks_list = []

        # UI elements
        self.master = master_ui  # Main window

        # Songs tab UI
        self.songs = SongsUiFrame(self.master.frm_tab_songs, self.click_btn_read, self.click_btn_apply,
                                  self.click_btn_sort, self.file_type_option_changed, self.sort_by_option_changed)
        # Playlist tab UI
        self.playlist = PlaylistUiFrame(self.master.frm_tab_playlist)

        # Download tab UI
        self.download = DownloadUiFrame(self.master.frm_tab_download)

        # Draw window using pack method
        self.master.pack()
        self.songs.pack()
        self.playlist.pack()
        self.download.pack()

        # Reset to default
        self.songs.set_default()
        self.set_filter_entry_default()

    def sort_by_option_changed(self, *args):
        so = self.songs
        so.sort_by = so.selected_sort_by_option.get().lower()

    def file_type_option_changed(self, *args):
        so = self.songs
        so.file_types = so.file_types_dict[so.selected_file_option.get()]

    def set_filter_entry_default(self):
        so = self.songs
        if so.ent_year.get() == '':
            so.ent_year.insert(0, 'Year')
        if so.ent_title.get() == '':
            so.ent_title.insert(0, 'Title')
        if so.ent_artist.get() == '':
            so.ent_artist.insert(0, 'Artist')
        if so.ent_genre.get() == '':
            so.ent_genre.insert(0, 'Genre')

    def draw_songs_list(self):
        so = self.songs
        so.lst.delete(0, END)
        for song in self.audio_tracks_list:
            if self.filter_metadata == song:
                so.insert_to_end_of_list(f'{song.artist} - {song.title}')

    def click_btn_sort(self):
        self.audio_tracks_list = sort_audio_tracks_list(self.audio_tracks_list, self.songs.sort_by)
        self.draw_songs_list()

    def click_btn_read(self):
        folder_path = ''
        so = self.songs
        try:
            folder_path = so.ent_path.get()
            audio_files = get_file_names_in_folder(folder_path, so.file_types)
        except FileNotFoundError:
            # Invalid path, so we need to run file dialog.
            folder_path = askdirectory()
            so.ent_path.delete(0, 'end')
            so.ent_path.insert(0, folder_path)
            audio_files = get_file_names_in_folder(folder_path, so.file_types)
        self.set_filter_entry_default()

        def read_folder(app_self):
            songs = app_self.songs
            count_of_files = len(audio_files)
            if count_of_files == 0:
                songs.insert_to_end_of_list('No audio files found')

            app_self.audio_tracks_list[:] = []
            file_index = 0

            for audio_file in audio_files:
                percent = file_index * 100 / count_of_files
                if songs.progress_bar['value'] != percent:
                    songs.progress_bar['value'] = percent
                audio_metadata_item = AudioTrackMp3(f'{folder_path}\\{audio_file}') if audio_file.endswith('mp3') else \
                    AudioTrackFlac(f'{folder_path}\\{audio_file}')
                app_self.audio_tracks_list.append(audio_metadata_item)
                file_index += 1

            songs.progress_bar['value'] = 100

            showinfo("Success", f"{file_index} files found")

            songs.progress_bar['value'] = 0
            self.draw_songs_list()

        thread = threading.Thread(target=read_folder, args=(self,))
        thread.start()

    def click_btn_apply(self):
        self.set_filter_entry_default()
        self.filter_metadata = AudioTrackFilter()

        so = self.songs

        if so.ent_title.get() != 'Title':
            self.filter_metadata.title = so.ent_title.get()
        if so.ent_artist.get() != 'Artist':
            self.filter_metadata.artist = so.ent_artist.get()
        if so.ent_genre.get() != 'Genre':
            self.filter_metadata.genre = so.ent_genre.get()
        if so.ent_year.get() != 'Year':
            year = int(so.ent_year.get())
            self.filter_metadata.year_ignore = False
            self.filter_metadata.year_min = year - 1
            self.filter_metadata.year_max = year + 1
        self.draw_songs_list()


def main():
    root = DefaultMainUi()

    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
