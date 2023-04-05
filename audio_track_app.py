from dev_tools import get_file_names_in_folder
import tkinter as tk
from tkinter import *
from audio_track import *


class App:
    def __init__(self, master):
        self.master = master
        self.listbox = tk.Listbox(self.master, width=100, height=30)
        self.listbox.pack(fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.listbox)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.button_read = tk.Button(self.master, text="Read folder", command=self.click_button_read)
        self.button_read.pack()

        self.entry = tk.Entry(self.master)
        self.entry.pack()

    def click_button_read(self):
        folder_path = self.entry.get()
        # Search all mp3 files in folder
        mp3_files = get_file_names_in_folder(folder_path, 'mp3')

        count_of_files = len(mp3_files)
        if count_of_files == 0:
            self.listbox.insert(tk.END, 'No MP3 files found')

        audio_tracks_list = []

        for mp3_file in mp3_files:
            audio_tracks_list.append(AudioTrackMp3(f'{folder_path}\\{mp3_file}'))

        filter_mp3 = AudioTrackFilter()
        # filter_mp3.artist = 'Queen'

        for song in audio_tracks_list:
            if filter_mp3 == song:
                self.listbox.insert(tk.END, f'{song.artist} - {song.title}')


root = tk.Tk()
root.geometry('620x500')

app = App(root)
root.mainloop()
