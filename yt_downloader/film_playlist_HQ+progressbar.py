import pytube #21.07.2022
from pytube import YouTube
from pytube.cli import on_progress
# if you are running it in windows, remember to change '\' to '/' in the path,
# because '\' in string has its own function - makes new line
# for example: good one: C:/Users/<Username>/Desktop/ytgui/audioplaylisttest
SAVE_PATH = ""
link = ''

try:
    playlist = pytube.Playlist(link)
    count_ = 1
    total = str(playlist.length)
    for video in playlist.videos:
        temp_link = video.watch_url
        yt = YouTube(temp_link,on_progress_callback=on_progress)
        try:  
            print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
            count_ += 1
        except: 
            print("some problem occured during dowloading!")
except: 
    print("connection with playlist failed")


