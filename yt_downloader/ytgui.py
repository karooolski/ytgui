# GUI -------------------------------------
import tkinter
from tkinter import ttk
#from tkinter import messagebox, filedialog # TODO may be useful in the future
import tkinter.font as font
# PYTUBE API ------------------------------
from pytube import Playlist
from pytube import YouTube 
from pytube.cli import on_progress #this module contains the built in progress bar. 
# System -------------------------------------------------
import os
from datetime import datetime
import requests
# EDIT METADATA of the file -----------------------------
import eyed3
from eyed3.id3.frames import ImageFrame
#from eyed3.id3 import tag
import eyed3.id3 as id3

# Convert video 1080p (no-voice) with audio ---------------------
import ffmpeg
# + pip install ffmpeg-python 
# + download GPL version of ffmpeg from https://github.com/BtbN/FFmpeg-Builds/releases and paste an '.exe' file in the project 
# + on windows add bin folder path of downlaoded GPL version to the PATH in global variables

# Convert mp4 -> mp3 ------------------------------------
from moviepy.audio.io import AudioFileClip
from moviepy.audio.AudioClip import *  # write_audiofile
from moviepy.audio.io.AudioFileClip import * # close

class DownloadType:
    downloadTypes = [
        "video 720p MAX",
        "audio mp3 with thumbnail",
        "audio mp3 playlist with thumbnails",
        "audio mp3",
        "audio playlist mp3",
        "audio mp4",
        "audio playlist mp4",
        "video playlist 720p MAX",
        "video 1080p and merge with audio",
        "video in 1080p with no Voice",
        "video (Lowest quality)",
        "video playlist (Lowest quality)"
    ]

# # GUI options 
#---------------

ASCI_grey = "#808080"
dark_cyan = "#308080"
main_collor = dark_cyan
TEXT_collor = "white"
TEXT_warning = "red"
gui_font = 'Helvetica'
gui_font_size = 15

# # Download Functions : Audios 
# -----------------------------

def download_mp3_audio_with_thumbnail(link,SAVE_PATH): 
    link = playlistOrNot(link,"single_video")
    try:
         yt = YouTube(link,on_progress_callback=on_progress)
    except:
         ("mp3 download connection error")
    try:
        audio = download_audio(yt,"mp3", SAVE_PATH)
        file_path = ""
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            print("couldnt convert mp4 to mp3")
        try: 
            # download video thumbnail
            yt_image = requests.get(yt.thumbnail_url)
            with open(os.path.join(SAVE_PATH,"thumbnail.jpg"),'wb') as f: 
                f.write(yt_image.content)
            # convert audio meta data
            audiofile = eyed3.load(file_path)
            if not audiofile.tag:
                audiofile.initTag()
            tag = id3.Tag()
            tag.parse(file_path)
            tag.title = yt.title
            tag.artist = yt.author
            tag.artist_url = link
            tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'thumbnail.jpg'),'rb').read(), 'image/jpeg')
            tag.save(version=eyed3.id3.ID3_V2_3)
            remove_file(SAVE_PATH,"thumbnail.jpg")
            # you can see a thumbnail using VLC media player, or something else
        except:
            print("Couldn`t make an image to file "+file_path)
        
    except:
        print("download_mp3_audio_with_thumbnail: (function) dowloading error!")    

def download_mp4_audio(link,SAVE_PATH):
    link = playlistOrNot(link,"single_video")
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        yt.streams.get_audio_only("mp4").download(SAVE_PATH)
    except:
        print("yt.streams.get_audio_only: error!")

# Usage: download video in 1080p and merge with audio
def downloadAudioToBeMerged(link,SAVE_PATH):   #download audio onldy
    global title       # variable for merge and rename purposes
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        #yt.streams.filter(abr="160kbps", progressive=False).first().download(SAVE_PATH,filename="audiocbd")
        yt.streams.get_audio_only("mp4").download(SAVE_PATH,filename="audiomerge.mp4")
        title = yt.title
    except: 
        print("Download audio failed")

def download_mp3_audio(link,SAVE_PATH):
    link = playlistOrNot(link,"single_video")
    try:
         yt = YouTube(link,on_progress_callback=on_progress)
    except:
         ("mp3 download connection error")
    try:
        audio = download_audio(yt,"mp3", SAVE_PATH)
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            print("couldnt convert mp4 to mp3")
    except:
        print("audio mp3 dowloading error!")


# # Download Functions : Videos
# -----------------------------

# Usage: download video in 1080p and merge with audio
def downloadVideo_1080p_toBeMerged(link,SAVE_PATH):   #download video only
    try:  
        yt = YouTube(link,on_progress_callback=on_progress)
        yt.streams.filter(res="1080p", progressive=False).first().download(SAVE_PATH,filename="videomerge.mp4")
    except:
        print("Download video failed")    

# usage: downloading mp3
def download_audio(yt: YouTube, file_type: str, downloads_path: str):
    try:
    # Download a video and debug progress
        if file_type == "mp4":
            audio = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        else:
            audio = yt.streams.filter(only_audio=True).get_audio_only() # it is mp4 too
        audio.download(downloads_path)
        return audio # returning audiofile (mp4) to be converted to mp3 
    except: 
        print("download video (function) error!")

def download_video_720pMAX(link,SAVE_PATH):
    try: 
        yt = YouTube(link,on_progress_callback=on_progress) 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH) 
    except: 
        print("download_video_720pMAX error!\n Do you set the PATH correctly?")

def download_video_LQ(link,SAVE_PATH):
    link = playlistOrNot(link,"single_video")
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        stream = yt.streams.first()
        stream.download(SAVE_PATH)
    except:
        print("download_video_LQ: error!")

def downloadVideoWithRezolution(SAVE_PATH,link,rezolution):
    try:
        yt = YouTube(link,on_progress_callback=on_progress) 
        yt.streams.filter(res=rezolution, progressive=False).first().download(SAVE_PATH)
    except: 
        print("Download video in ",str(rezolution),"p failed")


# # Download Functions : Playlists : Videos
# -----------------------------------------

def download_video_playlist_720pMAX(link,SAVE_PATH):
    link = playlistOrNot(link,"playlist")
    try:
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),str(total),str(video.title))
                #print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
                count_ += 1
            except:
                print("download_video_playlist_720pMAX: fail during downloading")
    except:
        print("download_video_playlist_720pMAX: error!")  

def download_video_playlist_LQ(link,SAVE_PATH):
    link = playlistOrNot(link,"playlist")
    try:
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),str(total),str(video.title))
                #print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
                stream = yt.streams.first()
                stream.download(SAVE_PATH)
                count_ += 1
            except:
                print("download_video_playlist_720pMAX: fail during downloading")
    except:
        print("download_video_playlist_720pMAX: error!")  

# # Download Functions : Playlists : Audios
#------------------------------------------

def download_mp3_audio_playlist_with_thumbnails(link,SAVE_PATH):
    try:
        link = playlistOrNot(link,"playlist")
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            file_path = ""
            try:
                print_info_downloading_playlist(str(count_),str(total),str(video.title))
                #print("downloading (",str(count_),"/",str(total),") ",video.title)
                audio = download_audio(yt,"mp3", SAVE_PATH)
                file_path = os.path.join(SAVE_PATH, audio.default_filename)
                file_path = convert_to_mp3_with_metadata(file_path)
                count_ += 1
            except:
                print("some problem occured during dowloading!")
            try:
               # download video thumbnail
                yt_image = requests.get(yt.thumbnail_url)  
                with open(os.path.join(SAVE_PATH,"thumbnail.jpg"),'wb') as f: 
                    f.write(yt_image.content)
                # convert audio meta data
                audiofile = eyed3.load(file_path)
                if not audiofile.tag:
                    audiofile.initTag()   
                tag = id3.Tag()    
                tag.parse(file_path)
                tag.title = yt.title
                tag.artist = yt.author
                tag.artist_url = link
                try:
                    tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'thumbnail.jpg'),'rb').read(), 'image/jpeg')
                except:
                    print("couldnt make an image by using tag")
                tag.save(version=eyed3.id3.ID3_V2_3) # important if u want to see effect also in windwos media player
                remove_file(SAVE_PATH,"thumbnail.jpg")             
            except:
                print("Couldn`t make an image to file "+file_path)
    except:
        print("Erorr during downloading palylist")
        print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")          

def download_mp3_audio_playlist(link,SAVE_PATH):
    try:
        link = playlistOrNot(link,"playlist")
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),str(total),str(video.title))
                #instead print("downloading (",str(count_),"/",str(total),") ",video.title)
                audio = download_audio(yt,"mp3", SAVE_PATH)
                file_path = os.path.join(SAVE_PATH, audio.default_filename)
                file_path = convert_to_mp3_with_metadata(file_path)
                count_ += 1
            except:
                print("download_mp3_audio_playlist_f(): some problem occured during dowloading!")
    except:
        print("Erorr during downloading palylist")
        print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")  


def download_mp4_audio_playlist(link,SAVE_PATH):
    try:
        link = playlistOrNot(link,"playlist")
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),str(total),str(video.title))
                #print("downloading (",str(count_),"/",str(total),") ",video.title)
                try:
                    yt.streams.get_audio_only("mp4").download(SAVE_PATH)
                except: print("download_mp4_audio_playlist: Stream download error")
                count_ += 1
            except:
                print("some problem occured during dowloading!")
    except:
        print("Erorr during downloading palylist")
        print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")

# # Editing Files Functions
# -------------------------

def remove_file(location,filename):
    path = os.path.join(location,filename)
    os.remove(path)
        
# Usage: download video in 1080p and merge with audio
def merge_video_with_audio():
    try:
        audio_path  = SAVE_PATH+'/'+"videomerge.mp4"
        video_path  = SAVE_PATH+'/'+"audiomerge.mp4"
        merged_video_path = SAVE_PATH+"/"+"output"+".mp4"
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(audio_path)
        ffmpeg.output(audio, video,merged_video_path).run(overwrite_output=True)
        remove_file(SAVE_PATH,"videomerge.mp4")
        remove_file(SAVE_PATH,"audiomerge.mp4")
        print("Merge ended successfully")
    except:
        print("Merge failed")

# usage: downloading mp3
def convert_to_mp3_with_metadata(file_path: str) -> str:
    try:
        # Use moviepy to convert an mp4 to an mp3 with metadata support. Delete mp4 afterwards
        try:
            audio_clip = AudioFileClip(file_path)
            try:
                file_path = file_path.replace("mp4", "mp3")
                audio_clip.write_audiofile(file_path)
                audio_clip.close()
                try:
                    os.remove(file_path.replace("mp3", "mp4")) # remove mp4 file
                    return file_path
                except: print("couldnt remove mp4 temporary file")
            except: print("couldnt write and close audiofile")
        except: print("couldnt make AdioFileClip")
    except:
        print("convert_to_mp3_with_metadata function error!")

# # inside functions 
# -------------------

# this program also need '/' slashes in the path like in linux instead "\"
def change_backslashes(word):
    ex = '\\'
    l = list(word)
    for i in range(len(word)):
        #w = print(word[i])
        if l[i] == ex:
            l[i] = '/'
        s = ''.join(l)
    return(s)

def change_backslashes_to_windows_type(word):
    ex = '/'
    l = list(word)
    for i in range(len(word)):
        #w = print(word[i])
        if l[i] == ex:
            l[i] = '\\'
        s = ''.join(l)
    return(s)

def stringReplace(word,toReplace,replacement):
    ex = toReplace
    l = list(word)
    for i in range(len(word)):
        if l[i] == ex:
            l[i] = replacement
        s = ''.join(l)
    return(s)

def time_now():
    now =  datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time = stringReplace(date_time,'/','.')    
    return date_time

def print_info_downloading_playlist(count_: str, total: str , video_title):  
    print(time_now()," downloading (",str(count_),"/",str(total),") ",video_title)

def playlistOrNot(linkk,confirm):
    print("checking playlist or single video:")
    print(link)
    if link.__contains__('https://www.youtube.com/playlist?list=') and confirm == "playlist":
        print("playlist confirmed")
        return link
    if not (linkk.__contains__('https://www.youtube.com/playlist?list=')) and confirm == "single_video":
        print("single video confirmed")
        return link
    else:
        print("UserErorr: link adressing playlist, not one film")
        return ' ' # https://www.youtube.com/watch?v=uXKdU_Nm-Kk

# # Button Fucntions (Tkinter)
# ----------------------------

def enableDownloadButton():
    if ButtonDownload["state"] == "disabled":
        ButtonDownload["state"] = "normal" #other options: active

def buttonActionConfirmThePath():
    global SAVE_PATH
    SAVE_PATH = textBoxPath.get(1.0, "end-1c")
    SAVE_PATH = change_backslashes(SAVE_PATH)
    labelPath.config(text = "Provided Input: "+SAVE_PATH)
    enableDownloadButton()
    
def startDownloading():
    global link 
    global SAVE_PATH
    link = textBoxDownloadLink.get(1.0, "end-1c")
    #label_download.config(text = "Provided Input: "+link)  
    chosen_plan = Combobox.get()
    print("Try download a video\nlink: ",link,"\nSAVE_PATH:",SAVE_PATH)
    
    if chosen_plan == "video 720p MAX":
        download_video_720pMAX(link,SAVE_PATH)
            
    if chosen_plan == "audio mp3 with thumbnail":
        download_mp3_audio_with_thumbnail(link,SAVE_PATH) 
        
    if chosen_plan == "audio mp3 playlist with thumbnails":
        download_mp3_audio_playlist_with_thumbnails(link,SAVE_PATH) 
         
    if chosen_plan == "audio mp3":
        download_mp3_audio(link,SAVE_PATH)
         
    if chosen_plan == "audio playlist mp3":
         download_mp3_audio_playlist(link,SAVE_PATH)
         
    if chosen_plan == "audio mp4":
         download_mp4_audio(link,SAVE_PATH)
         
    if chosen_plan == "audio playlist mp4":
        download_mp4_audio_playlist(link,SAVE_PATH)
         
    if chosen_plan == "video playlist 720p MAX":
        download_video_playlist_720pMAX(link,SAVE_PATH)
        
    if chosen_plan == "video 1080p and merge with audio":
        downloadVideo_1080p_toBeMerged(link,SAVE_PATH)
        downloadAudioToBeMerged(link,SAVE_PATH)
        merge_video_with_audio()
       
    if chosen_plan == "video in 1080p with no Voice":
        downloadVideoWithRezolution(SAVE_PATH,link,"1080p") # other: 1440p , 2160p
        
    if chosen_plan == "video (Lowest quality)":
        download_video_LQ(link,SAVE_PATH)
        
    if chosen_plan == "video playlist (Lowest quality)":
        download_video_playlist_LQ(link,SAVE_PATH) 

#def browse(): # TODO , not working yet
#    global SAVE_PATH
#    try:
#        download = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
#        SAVE_PATH = download
#        SAVE_PATH = change_backslashes(SAVE_PATH) # for windows usage 
#        textBoxPath.configure(text=str(SAVE_PATH))
#        print(SAVE_PATH)
#    except:
#        print("ygui: Browse (function) error!")
        
# -------|
# # Main |
# -------|

global SAVE_PATH
SAVE_PATH = ""
global link 
link = ""



def main():

    global textBoxPath
    global ButtonDownload
    global labelPath
    global textBoxDownloadLink
    global Combobox

    print(time_now())

    # Top level window -------------------------

    frame = tkinter.Tk()
    frame.title("YouTube Audio / Video Downloader")
    frame.geometry('500x350')
    frame.configure(background=main_collor)
    myFont = font.Font(family=gui_font, size=gui_font_size)

    # textbox for the path ----------------------

    textBoxPath = tkinter.Text(frame,height = 5,width = 20) # TextBox Creation
    textBoxPath.pack()

    # Label with info <enetering the path> ------

    labelPath = tkinter.Label(frame, text = "Enter here^ a PATH where to download:^",background=main_collor,fg=TEXT_collor)
    labelPath['font'] = myFont
    labelPath.pack()

    # Button Creation

    # Button to confirm tha path ----------------

    ButtonPathConfirm = tkinter.Button(frame,text = "confirm the PATH", command = buttonActionConfirmThePath)
    ButtonPathConfirm['font'] = myFont
    ButtonPathConfirm.pack()

    # Browse Button TODO -----------------------

    # Label Creation
    #browse_B = tkinter.Button(frame,text="Browse",command=Browse,width=10,bg="bisque",relief=GROOVE)
    #browse_B.pack()
    #browse_B.grid(row=3,
    #              column=2,
    #              pady=1,
    #              padx=1)

    #browseButton = tkinter.Button(frame,text="browse",command=browse)
    #browseButton.pack()

    # Textbox for the link ----------------------

    textBoxDownloadLink = tkinter.Text(frame,height = 5,width = 20)  
    textBoxDownloadLink.pack()

    # Label with info for the <confirm the path>

    label_download = tkinter.Label(frame,text="Enter here a YouTube Link ^", background=main_collor,fg=TEXT_collor)
    label_download['font'] = myFont
    label_download.pack()

    # Button to confirm download ----------------

    ButtonDownload = tkinter.Button(frame,text = "confirm link and download", command = startDownloading ) #buttonActionDownload
    ButtonDownload.pack()
    ButtonDownload["state"] = "disabled"  # button is disabled at start 
    ButtonDownload['font'] = myFont

    # Combobox to choose an option of download---

    dtt = DownloadType
    Combobox=ttk.Combobox(frame,values=dtt.downloadTypes,width=30,state = "readonly",font=myFont)
    Combobox.current(0) # show first option 
    frame.option_add('*TCombobox*Listbox.font', myFont) # apply font to combobox list
    Combobox.pack()

    frame.mainloop()

main()
