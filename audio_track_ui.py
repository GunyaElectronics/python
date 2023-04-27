import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
import tkinter.font as tk_font
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO


class DefaultMainUi(Tk):
    def __init__(self):
        super().__init__()
        # Notebook for select frame of the app
        self.ntb_base = ttk.Notebook(self)

        # Main window frames
        self.frm_tab_songs = tk.Frame(self.ntb_base)
        self.frm_tab_playlist = tk.Frame(self.ntb_base)
        self.frm_tab_download = tk.Frame(self.ntb_base)
        self.frm_tab_edit = tk.Frame(self.ntb_base)
        self.ntb_base.add(self.frm_tab_songs, text='Your Songs')
        self.ntb_base.add(self.frm_tab_playlist, text='Playlist')
        self.ntb_base.add(self.frm_tab_download, text='Download')
        self.ntb_base.add(self.frm_tab_edit, text='Edit')
        self.geometry('720x720')
        self.title('Audio Metadata Analyzer V0.2')

    def pack(self):
        self.ntb_base.pack(fill='both', expand=True)


def dummy_label(frame, font_size):
    font = tk_font.Font(size=font_size)
    lbl_dummy = tk.Label(frame, text='', font=font)
    lbl_dummy.pack()


class DefaultUiFrame:
    def __init__(self, frm_master):
        self.frm_visual = tk.Frame(frm_master)  # Frame with visual info, like listbox, scroll and progress bars.
        self.frm_buttons = tk.Frame(frm_master)  # Frame with your all control buttons and text inputs.
        elements_width = 33
        self.buttons_elements_width = elements_width
        self.options_elements_width = elements_width
        self.entry_elements_width = elements_width + 7

    def pack(self):
        self.frm_visual.pack(side=LEFT, fill=BOTH, expand=True)
        self.frm_buttons.pack()

    def entry(self):
        return tk.Entry(self.frm_buttons, width=self.entry_elements_width)

    def button(self, txt, cmd):
        return tk.Button(self.frm_buttons, text=txt, command=cmd, width=self.buttons_elements_width)

    def progressbar(self):
        return Progressbar(self.frm_visual, orient=HORIZONTAL, length=200, mode='determinate')

    def option_config_width(self, menu):
        menu.config(width=self.options_elements_width)

    def indent_on_buttons_frame(self, size=12):
        dummy_label(self.frm_buttons, size)

    def indent_on_visual_frame(self, size=12):
        dummy_label(self.frm_visual, size)

    def label(self, txt='', size=10):
        font = tk_font.Font(size=size)
        return tk.Label(self.frm_buttons, text=txt, font=font, width=self.buttons_elements_width, anchor="w")


class FrameWithListbox(DefaultUiFrame):
    def __init__(self, frm_master):
        super().__init__(frm_master)
        self.lst = tk.Listbox(self.frm_visual, width=100, height=30, selectmode=SINGLE)
        self._lst_user_indexes = []

        self.scrollbar = Scrollbar(self.lst)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.lst.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lst.yview)

        self.lbl_title = self.label()
        self.lbl_artist = self.label()
        self.lbl_album = self.label()
        self.lbl_year = self.label()
        self.lbl_genre = self.label()

        self.lbl_album_art = tk.Label(self.frm_buttons)

    def pack(self):
        super().pack()
        self.lst.pack(fill=BOTH, expand=True)

    def insert_to_end_of_list(self, text, index):
        self.lst.insert(tk.END, text)
        self._lst_user_indexes.append(index)

    def get_selected_lst_index(self):
        if len(self.lst.curselection()) > 0:
            return self.lst.curselection()[0]
        return None

    def remove_selected_lst_item(self):
        if len(self.lst.curselection()) == 0:
            return
        index = self.lst.curselection()[0]
        self._lst_user_indexes.pop(index)
        self.lst.delete(index, index)

    def remove_selected_lst_items(self):
        for index in self.lst.curselection():
            self._lst_user_indexes.pop(index)
            self.lst.delete(index, index)

    def get_selected_user_index(self):
        if len(self.lst.curselection()) > 0:
            return self._lst_user_indexes[self.lst.curselection()[0]]
        return None

    def get_all_selected_user_indexes(self):
        lst = []
        for sel in self.lst.curselection():
            lst.append(self._lst_user_indexes[sel])
        return lst

    def bind_select_lst_item_callback(self, callback):
        self.lst.bind('<<ListboxSelect>>', callback)

    def bind_double_click_lst_item_callback(self, callback):
        self.lst.bind('<Double-Button-1>', callback)

    def lst_delete_all(self):
        self.lst.delete(0, END)
        self._lst_user_indexes[:] = []

    def draw_track_metadata(self, track=None):
        t = track
        if t is None:
            self.lbl_title.configure(text='')
            self.lbl_artist.configure(text='')
            self.lbl_album.configure(text='')
            self.lbl_year.configure(text='')
            self.lbl_genre.configure(text='')
            self.lbl_album_art.image = None
            self.lbl_album_art.config(image='')
            self.lbl_album_art.update()
            return
        self.lbl_title.configure(text=f'   Title:\t{t.title}')
        self.lbl_artist.configure(text=f'   Artist:\t{t.artist}')
        self.lbl_album.configure(text=f'   Album:\t{t.album}')
        self.lbl_year.configure(text=f'   Year:\t{t.year}')
        self.lbl_genre.configure(text=f'   Genre:\t{t.genre}')
        if t.is_have_cover_art:
            pil_image = Image.open(BytesIO(t.cover_art))
            new_image = pil_image.resize((240, 240))
            tk_image = ImageTk.PhotoImage(new_image)
            self.lbl_album_art.image = tk_image
            self.lbl_album_art.config(image=tk_image)
        else:
            self.lbl_album_art.image = None
            self.lbl_album_art.config(image='')
            self.lbl_album_art.update()


def askdirectory():
    return filedialog.askdirectory()


def showinfo(result, info):
    messagebox.showinfo(result, info)


class SongsUiFrame(FrameWithListbox):
    def __init__(self, frm_master, click_btn_read, click_btn_apply, click_btn_sort, file_type_option_changed,
                 sort_by_option_changed, click_btn_add):
        super().__init__(frm_master)

        self.progress_bar = self.progressbar()
        self.progress_bar['value'] = 0

        self.btn_read = self.button(txt="Read folder content", cmd=click_btn_read)
        self.btn_apply = self.button(txt="Apply filter", cmd=click_btn_apply)
        self.btn_sort = self.button(txt="Sort songs", cmd=click_btn_sort)
        self.btn_add_to_pl = self.button(txt='Add to playlist', cmd=click_btn_add)

        self.ent_path = self.entry()
        self.ent_artist = self.entry()
        self.ent_title = self.entry()
        self.ent_genre = self.entry()
        self.ent_year = self.entry()

        self.file_types_dict = {'Search all files': ['mp3', 'flac'],
                                'Search mp3 only': ['mp3'],
                                'Search flac only': ['flac']
                                }
        self.file_types = self.file_types_dict['Search all files']
        self.file_type_options = list(self.file_types_dict.keys())
        self.selected_file_option = tk.StringVar(value=self.file_type_options[0])

        self.selected_file_option.trace('w', file_type_option_changed)
        self.option_selected_file_menu = tk.OptionMenu(self.frm_buttons, self.selected_file_option,
                                                       *self.file_type_options)
        self.option_config_width(self.option_selected_file_menu)

        self.sort_by_options = ['Artist', 'Title', 'Genre', 'Album']
        self.sort_by = self.sort_by_options[0].lower()
        self.selected_sort_by_option = tk.StringVar(value=self.sort_by_options[0])
        self.selected_sort_by_option.trace('w', sort_by_option_changed)
        self.opt_sort_by_menu = tk.OptionMenu(self.frm_buttons, self.selected_sort_by_option, *self.sort_by_options)
        self.option_config_width(self.opt_sort_by_menu)

    def pack(self):
        super().pack()
        self.progress_bar.pack(fill=BOTH)
        self.ent_path.pack(side=TOP)
        self.option_selected_file_menu.pack()
        self.btn_read.pack()
        self.indent_on_buttons_frame()
        self.ent_artist.pack()
        self.ent_title.pack()
        self.ent_genre.pack()
        self.ent_year.pack()
        self.btn_apply.pack()
        self.indent_on_buttons_frame()
        self.opt_sort_by_menu.pack()
        self.btn_sort.pack()
        self.btn_add_to_pl.pack()
        self.indent_on_buttons_frame()
        self.lbl_title.pack()
        self.lbl_artist.pack()
        self.lbl_album.pack()
        self.lbl_year.pack()
        self.lbl_genre.pack()
        self.lbl_album_art.pack()

    def set_default(self):
        # Set default values
        self.ent_path.insert(0, 'Enter folder path..')


class PlaylistUiFrame(FrameWithListbox):
    def __init__(self, frm_master):
        super().__init__(frm_master)
        self.ent_path = self.entry()
        self.ent_path.insert(0, 'Folder path to save')
        self.btn_remove = self.button(txt='Remove', cmd=None)

    def pack(self):
        super().pack()
        self.ent_path.pack(side=TOP)
        self.btn_remove.pack()
        self.indent_on_buttons_frame()
        self.lbl_title.pack()
        self.lbl_artist.pack()
        self.lbl_album.pack()
        self.lbl_year.pack()
        self.lbl_genre.pack()
        self.lbl_album_art.pack()


class DownloadUiFrame(FrameWithListbox):
    def __init__(self, frm_master):
        super().__init__(frm_master)
        self.ent_phrase = self.entry()
        self.ent_phrase.insert(0, '')
        self.btn_search = self.button(txt='Search', cmd=None)

    def pack(self):
        super().pack()
        self.ent_phrase.pack(side=TOP)
        self.btn_search.pack()
