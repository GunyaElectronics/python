from dev_tools import get_file_names_in_folder
from audio_track_ui import *
from audio_track import *
import threading
import shutil
import os


def get_list_item_text(list_item):
    t = list_item.track
    if t.title == '' and t.artist == '':
        return f'{t.file_path}'
    return f'{t.artist} - {t.title}'


class App:
    def __init__(self, master_ui):
        # Algorithm elements
        self.filter_metadata = AudioTrackFilter()
        self.audio_tracks_list = []
        self.playlist_path = None

        # UI elements
        self.master = master_ui  # Main window

        # Songs tab UI
        self.songs = SongsUiFrame(self.master.frm_tab_songs, self.click_btn_read, self.click_btn_apply,
                                  self.click_btn_sort, self.file_type_option_changed, self.sort_by_option_changed,
                                  self.click_btn_add_item)
        # Playlist tab UI
        self.playlist = PlaylistUiFrame(self.master.frm_tab_playlist, self.click_btn_browse, self.click_btn_save)

        # Download tab UI
        self.download = DownloadUiFrame(self.master.frm_tab_download)

        # Bind another business logic callbacks
        self.songs.bind_double_click_lst_item_callback(self.song_lst_event_item_double_click)
        self.songs.bind_select_lst_item_callback(self.song_lst_event_item_selected)
        self.playlist.bind_select_lst_item_callback(self.playlist_lst_event_item_selected)
        # Draw window using pack method
        self.master.pack()
        self.songs.pack()
        self.playlist.pack()
        self.download.pack()

        # Reset to default
        self.songs.set_default()
        self.set_filter_entry_default()

    def sort_by_option_changed(self):
        so = self.songs
        so.sort_by = so.selected_sort_by_option.get().lower()

    def file_type_option_changed(self):
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
        so.lst_delete_all()
        for list_item in self.audio_tracks_list:
            if self.filter_metadata == list_item.track:
                so.insert_to_end_of_list(get_list_item_text(list_item), list_item.list_index)

    def click_btn_sort(self):
        self.audio_tracks_list = sort_audio_tracks_list(self.audio_tracks_list, f'track.{self.songs.sort_by}')
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
                play_list_item = PlaylistItem(audio_metadata_item)
                play_list_item.list_index = file_index
                app_self.audio_tracks_list.append(play_list_item)
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

    def _get_selected_playlist_item(self, s):
        index = s.get_selected_user_index()
        return None if index is None else self.audio_tracks_list[index]

    def song_lst_event_item_selected(self, event):
        s = self._get_selected_playlist_item(self.songs)
        self.songs.draw_track_metadata(s if not s else s.track)

    def playlist_lst_event_item_selected(self, event):
        s = self._get_selected_playlist_item(self.playlist)
        self.playlist.draw_track_metadata(s if not s else s.track)

    def song_lst_event_item_double_click(self, event):
        lst_item = self._get_selected_playlist_item(self.songs)
        if lst_item is None:
            return
        self.songs.remove_selected_lst_item()
        self.songs.draw_track_metadata()
        self.playlist.insert_to_end_of_list(get_list_item_text(lst_item), lst_item.list_index)

    def click_btn_add_item(self):
        indexes = self.songs.get_all_selected_user_indexes()
        if len(indexes):
            self.songs.draw_track_metadata()
        self.songs.remove_selected_lst_items()
        for itm in indexes:
            itm = self.audio_tracks_list[itm]
            self.playlist.insert_to_end_of_list(get_list_item_text(itm), itm.list_index)

    def click_btn_browse(self):
        self.playlist_path = askdirectory()
        self.playlist.set_entry_text(self.playlist_path)

    def click_btn_save(self):
        for index in self.playlist.get_all_user_indexes():
            full_path = self.audio_tracks_list[index].track.file_path
            name = os.path.basename(full_path)
            shutil.copy(full_path, f'{self.playlist_path}/{name}')
            print(f'Copy "{name}" to the "{self.playlist_path}" folder')


def main():
    root = DefaultMainUi()

    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
