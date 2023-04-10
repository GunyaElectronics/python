import moviepy.editor as mp
from PIL import Image
import zlib
import os


class MyAudioExtractor:
    def __init__(self, file_in, file_result=None):
        self.file_in = file_in
        if file_result is None:
            self.file_result = file_in.replace('.mp4', '.mp3')

    def convert_to_mp3(self):
        try:
            video = mp.VideoFileClip(self.file_in)
            print(f'The input file is {self.file_in}. Try convert to the {self.file_result}')
            video.audio.write_audiofile(self.file_result)
        except FileExistsError:
            print('File already exist')


def get_jpg_from_webp(file_webp, jpg_result=None):
    with Image.open(file_webp) as im:
        im = im.convert('RGB')
        if jpg_result is None:
            jpg_result = file_webp.replace('.webp', '.jpg')
        im.save(jpg_result, 'JPEG')


def calculate_crc32(file_name, print_enable=False):
    with open(file_name, 'rb') as f:
        buf = f.read()
        crc32 = zlib.crc32(buf)
        if print_enable:
            print(f'CRC32: {crc32:08X}')
        return crc32


def get_file_names_in_folder(directory, fileendwith=None):
    if fileendwith is None:
        return []

    file_names_list = []
    for f in os.listdir(directory):
        for key in fileendwith:
            if f.endswith(key):
                file_names_list.append(f)
    return file_names_list


def file_size(file_name):
    return os.path.getsize(file_name)
