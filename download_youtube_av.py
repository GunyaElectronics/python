from pytube import YouTube
from dev_tools import get_file_names_in_folder, MyAudioExtractor


def download(link_tube):
    try:
        youtube_object = YouTube(link_tube)
        youtube_object = youtube_object.streams.get_highest_resolution()
        youtube_object.download()
    except:
        print("An error has occurred")
    else:
        print("Download is completed successfully")


filename = 'C:\\path\\file.html'


def find_youtube_video_link(line_for_search):
    return True if 'https://www.youtube.com/watch?v=' in line_for_search else False


def get_youtube_video_link(line_with_link):
    start = line_with_link.find('https:/')
    end = line_with_link.find('">', line_with_link.find('watch?v='))
    if '&amp' in line_with_link:
        end = line_with_link.find('&amp')
    lnk = line_with_link[start:end]
    return lnk if len(lnk) == len('https://www.youtube.com/watch?v=xxxxxxxxxxx') else None


with open(filename, 'r', encoding="utf8") as f:
    links = []
    for line in f:
        if find_youtube_video_link(line) and get_youtube_video_link(line):
            links.append(get_youtube_video_link(line))

    # Remove copy of links
    new_links = []
    for item in links:
        if item not in new_links:
            new_links.append(item)

    links = new_links

    print(f'{len(links)} videos found..')

    for link in links:
        print(link)
        download(link)

    print('Downloading done.')

    files = get_file_names_in_folder('D:\Music', 'mp4')

    # Convert all mp4 videos to the mp3 audio files
    for f in files:
        ob = MyAudioExtractor(f)
        ob.convert_to_mp3()

    print('Converting done')
