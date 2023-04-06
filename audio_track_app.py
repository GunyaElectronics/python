from dev_tools import get_file_names_in_folder
import threading
from audio_track import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import tkinter as tk


class App:
    def __init__(self, master_ui):

        # Algorithm elements
        self.filter_mp3 = AudioTrackFilter()
        self.audio_tracks_list = []

        # UI elements
        self.master = master_ui
        self.progress_bar = Progressbar(self.master, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress_bar['value'] = 0

        self.listbox = tk.Listbox(self.master, width=100, height=30)

        self.scrollbar = Scrollbar(self.listbox)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        elements_width = 33
        self.button_read = tk.Button(self.master, text="Read folder content", command=self.click_button_read,
                                     width=elements_width)
        self.button_apply = tk.Button(self.master, text="Apply filter", command=self.click_button_apply,
                                      width=elements_width)
        self.button_sort = tk.Button(self.master, text="Sort songs", command=self.click_button_read,
                                     width=elements_width)

        options = ["Search all files", "Search mp3 only", "Search flac only"]
        selected_option = tk.StringVar(value=options[0])

        self.option_menu = tk.OptionMenu(self.master, selected_option, *options)
        self.option_menu.config(width=elements_width)

        entry_width = 40
        self.entry_path = tk.Entry(self.master, width=entry_width)
        self.entry_artist = tk.Entry(self.master, width=entry_width)
        self.entry_title = tk.Entry(self.master, width=entry_width)
        self.entry_genre = tk.Entry(self.master, width=entry_width)
        self.entry_year = tk.Entry(self.master, width=entry_width)

        # Draw window using pack method
        self.listbox.pack(fill=BOTH, expand=True)
        self.progress_bar.pack(fill=BOTH)
        self.entry_path.pack(side=TOP)
        self.button_read.pack()
        self.entry_artist.pack()
        self.entry_title.pack()
        self.entry_genre.pack()
        self.entry_year.pack()
        self.button_apply.pack()
        self.button_sort.pack()
        self.option_menu.pack()

        # Set default values
        self.entry_path.insert(0, 'Enter folder path..')
        self.set_filter_entry_default()

    def set_filter_entry_default(self):
        if self.entry_year.get() == '':
            self.entry_year.insert(0, 'Year')
        if self.entry_title.get() == '':
            self.entry_title.insert(0, 'Title')
        if self.entry_artist.get() == '':
            self.entry_artist.insert(0, 'Artist')
        if self.entry_genre.get() == '':
            self.entry_genre.insert(0, 'Genre')

    def draw_songs_list(self):
        self.listbox.delete(0, END)
        for song in self.audio_tracks_list:
            if self.filter_mp3 == song:
                self.listbox.insert(tk.END, f'{song.artist} - {song.title}')

    def click_button_read(self):
        self.set_filter_entry_default()

        def read_folder(app_self):
            folder_path = app_self.entry_path.get()
            # Search all mp3 files in folder
            mp3_files = get_file_names_in_folder(folder_path, 'mp3')

            count_of_files = len(mp3_files)
            if count_of_files == 0:
                app_self.listbox.insert(tk.END, 'No MP3 files found')

            file_index = 0
            for mp3_file in mp3_files:
                percent = file_index * 100 / count_of_files
                if app_self.progress_bar['value'] != percent:
                    app_self.progress_bar['value'] = percent
                app_self.audio_tracks_list.append(AudioTrackMp3(f'{folder_path}\\{mp3_file}'))
                file_index += 1

            app_self.progress_bar['value'] = 100

            messagebox.showinfo("Success", f"{file_index} files found")

            app_self.progress_bar['value'] = 0
            self.draw_songs_list()

        thread = threading.Thread(target=read_folder, args=(self,))
        thread.start()

    def click_button_apply(self):
        self.set_filter_entry_default()
        self.filter_mp3 = AudioTrackFilter()

        if self.entry_title.get() != 'Title':
            self.filter_mp3.title = self.entry_title.get()
        if self.entry_artist.get() != 'Artist':
            self.filter_mp3.artist = self.entry_artist.get()
        if self.entry_genre.get() != 'Genre':
            self.filter_mp3.genre = self.entry_genre.get()
        if self.entry_year.get() != 'Year':
            year = int(self.entry_year.get())
            self.filter_mp3.year_ignore = False
            self.filter_mp3.year_min = year - 1
            self.filter_mp3.year_max = year + 1
        self.draw_songs_list()


def main():
    root = tk.Tk()
    root.geometry('720x600')

    app = App(root)
    root.title('MP3 metadata analyzer')
    root.mainloop()


if __name__ == '__main__':
    main()
