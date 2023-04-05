from dev_tools import get_file_names_in_folder
import tkinter as tk
from tkinter import *
from tkinter.ttk import Progressbar
from audio_track import *
import threading


class App:
    def __init__(self, master):
        self.master = master

        self.progress_bar = Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress_bar['value'] = 0

        self.listbox = tk.Listbox(self.master, width=100, height=30)
        self.listbox.pack(fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.listbox)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.button_read = tk.Button(self.master, text="Read folder", command=self.click_button_read)

        self.label = tk.Label(self.master, text='Enter folder path:')
        self.label.pack(side=LEFT)

        self.entry = tk.Entry(self.master, width=40)
        self.entry.pack(side=LEFT)
        self.button_read.pack(side=LEFT)
        self.progress_bar.pack(pady=10)

    def click_button_read(self):
        def read_folder(app_self):
            folder_path = app_self.entry.get()
            # Search all mp3 files in folder
            mp3_files = get_file_names_in_folder(folder_path, 'mp3')

            count_of_files = len(mp3_files)
            if count_of_files == 0:
                app_self.listbox.insert(tk.END, 'No MP3 files found')

            audio_tracks_list = []

            file_index = 0
            for mp3_file in mp3_files:
                percent = file_index * 100 / count_of_files
                if app_self.progress_bar['value'] != percent:
                    app_self.progress_bar['value'] = percent
                audio_tracks_list.append(AudioTrackMp3(f'{folder_path}\\{mp3_file}'))
                file_index += 1

            app_self.progress_bar['value'] = 100

            filter_mp3 = AudioTrackFilter()

            for song in audio_tracks_list:
                if filter_mp3 == song:
                    app_self.listbox.insert(tk.END, f'{song.artist} - {song.title}')

        thread = threading.Thread(target=read_folder, args=(self,))
        thread.start()


root = tk.Tk()
root.geometry('620x500')

app = App(root)
root.mainloop()
