from dev_tools import get_file_names_in_folder
import threading
from audio_track import *
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
import tkinter as tk


class App:
    def __init__(self, master_ui):

        # Algorithm elements
        self.filter_metadata = AudioTrackFilter()
        self.audio_tracks_list = []

        # UI elements
        self.master = master_ui  # Main window

        self.frm_visual_data = tk.Frame(self.master)  # Frame with listbox, scroll bar and progress bar.
        self.frm_buttons = tk.Frame(self.master)  # Frame with all control buttons and menus

        self.progress_bar = Progressbar(self.frm_visual_data, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress_bar['value'] = 0

        self.listbox = tk.Listbox(self.frm_visual_data, width=100, height=30)

        self.scrollbar = Scrollbar(self.listbox)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        elements_width = 33
        self.btn_read = tk.Button(self.frm_buttons, text="Read folder content", command=self.click_btn_read,
                                  width=elements_width)
        self.btn_apply = tk.Button(self.frm_buttons, text="Apply filter", command=self.click_btn_apply,
                                   width=elements_width)
        self.btn_sort = tk.Button(self.frm_buttons, text="Sort songs", command=self.click_btn_sort,
                                  width=elements_width)
        self.file_types_dict = {'Search all files': ['mp3', 'flac'],
                                'Search mp3 only': ['mp3'],
                                'Search flac only': ['flac']
                                }
        self.file_types = self.file_types_dict['Search all files']
        self.file_type_options = list(self.file_types_dict.keys())
        self.selected_file_option = tk.StringVar(value=self.file_type_options[0])

        self.selected_file_option.trace('w', self.file_type_option_changed)
        self.option_selected_file_menu = tk.OptionMenu(self.frm_buttons, self.selected_file_option,
                                                       *self.file_type_options)
        self.option_selected_file_menu.config(width=elements_width)

        self.sort_by_options = ['Artist', 'Title', 'Genre', 'Album']
        self.sort_by = self.sort_by_options[0].lower()
        self.selected_sort_by_option = tk.StringVar(value=self.sort_by_options[0])
        self.selected_sort_by_option.trace('w', self.sort_by_option_changed)
        self.opt_sort_by_menu = tk.OptionMenu(self.frm_buttons, self.selected_sort_by_option, *self.sort_by_options)
        self.opt_sort_by_menu.config(width=elements_width)

        entry_width = 40
        self.ent_path = tk.Entry(self.frm_buttons, width=entry_width)
        self.ent_artist = tk.Entry(self.frm_buttons, width=entry_width)
        self.ent_title = tk.Entry(self.frm_buttons, width=entry_width)
        self.ent_genre = tk.Entry(self.frm_buttons, width=entry_width)
        self.ent_year = tk.Entry(self.frm_buttons, width=entry_width)

        # Draw window using pack method
        self.frm_visual_data.pack(side=LEFT, fill=BOTH, expand=True)
        self.frm_buttons.pack()
        self.listbox.pack(fill=BOTH, expand=True)
        self.progress_bar.pack(fill=BOTH)
        self.ent_path.pack(side=TOP)
        self.option_selected_file_menu.pack()
        self.btn_read.pack()
        self.ent_artist.pack()
        self.ent_title.pack()
        self.ent_genre.pack()
        self.ent_year.pack()
        self.btn_apply.pack()
        self.opt_sort_by_menu.pack()
        self.btn_sort.pack()

        # Set default values
        self.ent_path.insert(0, 'Enter folder path..')
        self.set_filter_entry_default()

    def sort_by_option_changed(self, *args):
        self.sort_by = self.selected_sort_by_option.get().lower()

    def file_type_option_changed(self, *args):
        self.file_types = self.file_types_dict[self.selected_file_option.get()]

    def set_filter_entry_default(self):
        if self.ent_year.get() == '':
            self.ent_year.insert(0, 'Year')
        if self.ent_title.get() == '':
            self.ent_title.insert(0, 'Title')
        if self.ent_artist.get() == '':
            self.ent_artist.insert(0, 'Artist')
        if self.ent_genre.get() == '':
            self.ent_genre.insert(0, 'Genre')

    def draw_songs_list(self):
        self.listbox.delete(0, END)
        for song in self.audio_tracks_list:
            if self.filter_metadata == song:
                self.listbox.insert(tk.END, f'{song.artist} - {song.title}')

    def click_btn_sort(self):
        self.audio_tracks_list = sort_audio_tracks_list(self.audio_tracks_list, self.sort_by)
        self.draw_songs_list()

    def click_btn_read(self):
        folder_path = ''
        try:
            folder_path = self.ent_path.get()
            audio_files = get_file_names_in_folder(folder_path, self.file_types)
        except FileNotFoundError:
            # Invalid path, so we need to run file dialog.
            folder_path = filedialog.askdirectory()
            self.ent_path.delete(0, 'end')
            self.ent_path.insert(0, folder_path)
            audio_files = get_file_names_in_folder(folder_path, self.file_types)
        self.set_filter_entry_default()

        def read_folder(app_self):
            count_of_files = len(audio_files)
            if count_of_files == 0:
                app_self.listbox.insert(tk.END, 'No audio files found')

            app_self.audio_tracks_list[:] = []
            file_index = 0

            for audio_file in audio_files:
                percent = file_index * 100 / count_of_files
                if app_self.progress_bar['value'] != percent:
                    app_self.progress_bar['value'] = percent
                audio_metadata_item = AudioTrackMp3(f'{folder_path}\\{audio_file}') if audio_file.endswith('mp3') else \
                    AudioTrackFlac(f'{folder_path}\\{audio_file}')
                app_self.audio_tracks_list.append(audio_metadata_item)
                file_index += 1

            app_self.progress_bar['value'] = 100

            messagebox.showinfo("Success", f"{file_index} files found")

            app_self.progress_bar['value'] = 0
            self.draw_songs_list()

        thread = threading.Thread(target=read_folder, args=(self,))
        thread.start()

    def click_btn_apply(self):
        self.set_filter_entry_default()
        self.filter_metadata = AudioTrackFilter()

        if self.ent_title.get() != 'Title':
            self.filter_metadata.title = self.ent_title.get()
        if self.ent_artist.get() != 'Artist':
            self.filter_metadata.artist = self.ent_artist.get()
        if self.ent_genre.get() != 'Genre':
            self.filter_metadata.genre = self.ent_genre.get()
        if self.ent_year.get() != 'Year':
            year = int(self.ent_year.get())
            self.filter_metadata.year_ignore = False
            self.filter_metadata.year_min = year - 1
            self.filter_metadata.year_max = year + 1
        self.draw_songs_list()


def main():
    root = tk.Tk()
    root.geometry('720x600')

    app = App(root)
    root.title('Audio metadata analyzer')
    root.mainloop()


if __name__ == '__main__':
    main()
