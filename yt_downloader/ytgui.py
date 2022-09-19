# GUI -------------------------------------
import tkinter
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.font as font
#from tkinter import set
#from tkinter import *
#from turtle import color, position
# PYTUBE API ------------------------------
from pytube import Playlist
from pytube import YouTube 
from pytube.cli import on_progress #this module contains the built in progress bar. 
# System -------------------------------------------------
import time
import os
from datetime import datetime
import colorama
from colorama import Fore
import requests
# EDIT METADATA of the file -----------------------------
import eyed3
from eyed3.id3.frames import ImageFrame
from eyed3.id3 import tag
import eyed3.id3 as id3
##from eyed3.core import Tag
#from moviepy import *
#import eyed3.mp3.Mp3AudioFile #- For mp3 audio files.
#import eyed3.id3.TagFile #- For raw ID3 data files
# Convert 1080p (no-voice) with mp3 ---------------------
import ffmpeg
# Convert mp4 -> mp3 ------------------------------------
from moviepy.audio.io import AudioFileClip
from moviepy.audio.AudioClip import *  # write_audiofile
from moviepy.audio.io.AudioFileClip import * # close

#from moviepy.editor import AudioFileClip # pyinstaller zadziala ale nie zrobi mp3
#from moviepy.audio.io import AudioFileClip # earlier: from moviepy.editor import AudioFileClip
#from moviepy import *
#https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/

class downloadType:
    pizza = ""
    nalesniki = ""
    #course=["Pizza","Burger","Noodles","pierogi","schabowe","dobre_wedzone","piwo","woda","garnitur","kapsel","brukselka","jeczmien",
    #   "obwarzany","stokrotkowitowiczonawodniczywniczyrzyc"]
    course = [
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

class DonwnloadType: #TODO : To be filled instead global variables
    download_mp4_audio = 0
    download_mp3_audio = 0
    download_mp3_audio_with_thumbnail = 0
    download_mp3_audio_playlist = 0
    download_mp3_audio_playlist_with_thumbnails = 0
    download_mp4_audio_playlist = 0
    download_video_1080p = 0
    download_video_1080p_merge = 0  
    download_video_720pMAX = 1
    download_video_LQ = 0
    download_video_playlist_720pMAX = 0
    download_video_playlist_LQ = 0
    
    @classmethod
    def resetValues(self):
        self.download_mp4_audio = 0
        self.download_mp3_audio = 0
        self.download_mp3_audio_with_thumbnail = 0
        self.download_mp3_audio_playlist = 0
        self.download_mp3_audio_playlist_with_thumbnails = 0
        self.download_mp4_audio_playlist = 0
        self.download_video_1080p = 0
        self.download_video_1080p_merge = 0  
        self.download_video_720pMAX = 0
        self.download_video_LQ = 0
        self.download_video_playlist_720pMAX = 0
        self.download_video_playlist_LQ = 0

global currentMode
currentMode = 2

ASCI_grey = "#808080"
TEXT_collor = "white"
TEXT_warning = "red"

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

# # Download Functions : Audios 
# -----------------------------

def download_mp3_audio_with_thumbnail_f(link,SAVE_PATH): 
    link = playlistOrNot(link,"single_video")
    try:
         yt = YouTube(link,on_progress_callback=on_progress)
    except:
         ("mp3 download connection error")
    try:
        audio = download_video(yt,"mp3", SAVE_PATH)
        file_path = ""
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            print("couldnt convert mp4 to mp3")
        try: 
            # download video thumbnail
            yt_image = requests.get(yt.thumbnail_url)
            with open(os.path.join(SAVE_PATH,"szablon.jpg"),'wb') as f: 
                f.write(yt_image.content)
            # convert audio meta data
            audiofile = eyed3.load(file_path)
            if not audiofile.tag:
                audiofile.initTag()
            tag = id3.Tag()
            tag.parse(file_path)
            tag.title = yt.title
            tag.artist = yt.author
            tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'szablon.jpg'),'rb').read(), 'image/jpeg')
            tag.save(version=eyed3.id3.ID3_V2_3)
            remove_file(SAVE_PATH,"szablon.jpg")
            # you can see a thumbnail using VLC media player, on windows
        except:
            print("Couldn`t make an image to file "+file_path)
        
    except:
        print("download_mp3_audio_with_thumbnail_f: (function) dowloading error!")    

def download_mp4_audio_f(link,SAVE_PATH):
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

def download_mp3_audio_f(link,SAVE_PATH):
    link = playlistOrNot(link,"single_video")
    try:
         yt = YouTube(link,on_progress_callback=on_progress)
    except:
         ("mp3 download connection error")
    try:
        audio = download_video(yt,"mp3", SAVE_PATH)
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
def download_video(yt: YouTube, file_type: str, downloads_path: str):
    try:
    # Download a video and debug progress
        if file_type == "mp4":
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        else:
            video = yt.streams.filter(only_audio=True).get_audio_only()
        video.download(downloads_path)
        return video
    except: 
        print("download video (function) error!")

def download_video_720pMAX_f(link,SAVE_PATH):
    try: 
        yt = YouTube(link,on_progress_callback=on_progress) 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH) 
    except: 
        print("download_video_720pMAX error!\n Do you set the PATH correctly?")

def download_video_LQ_f(link,SAVE_PATH):
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

def download_video_playlist_720pMAX_f(link,SAVE_PATH):
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

def download_video_playlist_LQ_f(link,SAVE_PATH):
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

def download_mp3_audio_playlist_with_thumbnails_f(link,SAVE_PATH):
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
                audio = download_video(yt,"mp3", SAVE_PATH)
                file_path = os.path.join(SAVE_PATH, audio.default_filename)
                file_path = convert_to_mp3_with_metadata(file_path)
                count_ += 1
            except:
                print("some problem occured during dowloading!")
            try:
               # download video thumbnail
                yt_image = requests.get(yt.thumbnail_url)  
                with open(os.path.join(SAVE_PATH,"szablon.jpg"),'wb') as f: 
                    f.write(yt_image.content)
                # convert audio meta data
                audiofile = eyed3.load(file_path)
                if not audiofile.tag:
                    audiofile.initTag()   
                tag = id3.Tag()    
                tag.parse(file_path)
                tag.title = yt.title
                tag.artist = yt.author
                try:
                    tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'szablon.jpg'),'rb').read(), 'image/jpeg')
                except:
                    print("couldnt make an image by using tag")
                tag.save(version=eyed3.id3.ID3_V2_3) # important if u want to see effect also in windwos media player
                remove_file(SAVE_PATH,"szablon.jpg")             
            except:
                print("Couldn`t make an image to file "+file_path)
    except:
        print("Erorr during downloading palylist")
        print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")          

def download_mp3_audio_playlist_f(link,SAVE_PATH):
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
                audio = download_video(yt,"mp3", SAVE_PATH)
                file_path = os.path.join(SAVE_PATH, audio.default_filename)
                file_path = convert_to_mp3_with_metadata(file_path)
                count_ += 1
            except:
                print("download_mp3_audio_playlist_f(): some problem occured during dowloading!")
    except:
        print("Erorr during downloading palylist")
        print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")  


def download_mp4_audio_playlist_f(link,SAVE_PATH):
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
        input_audio_path = SAVE_PATH+'/'+"videomerge.mp4"
        input_video_path = SAVE_PATH+'/'+"audiomerge.mp4"
        output_video_path = SAVE_PATH+"/"+"output"+".mp4"
        video = ffmpeg.input(input_video_path)
        audio = ffmpeg.input(input_audio_path)
        ffmpeg.output(audio, video,output_video_path).run(overwrite_output=True)
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
            except: print("couldnt write and close adiofile")
        except: print("couldnt make AdioFileClip")
    except:
        print("convert_to_mp3_with_metadata function error!")

# # inside functions 
# ------------------

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


def resetValues(dt: DonwnloadType):    
    dt.resetValues()
    label_download.configure(background=ASCI_grey,text="You can change wether you want do download video / audio ^",fg=TEXT_collor)

#def changeDownladType():
#    # dt:DownladType is defined in main section 
#    global currentMode 
#
#    max_modes = 13  # count -1 , the last is a switcher to first mode
#    
#    if currentMode == 1:
#        resetValues(dt)
#        dt.download_video_720pMAX = 1 
#        ButtonAudioVideoDownloadChange.configure(text="1/12 Now you will download video (720p MAX)", command = changeDownladType)
#        print("downlading video mode ON (720p MAX)")
#
#    if currentMode == 2:
#        resetValues(dt)
#        dt.download_mp3_audio_with_thumbnail = 1
#        ButtonAudioVideoDownloadChange.configure(text="2/12 download audio mp3 with thumbnail",command = changeDownladType)
#    
#    if currentMode == 3:
#        resetValues(dt)
#        dt.download_mp3_audio_playlist_with_thumbnails = 1
#        ButtonAudioVideoDownloadChange.configure(text="3/12 download audio mp3 playlist with thumbnails",command = changeDownladType)
#
#    if currentMode == 4: 
#        resetValues(dt)
#        dt.download_mp3_audio = 1
#        ButtonAudioVideoDownloadChange.configure(text="4/12 Now you will download audio (mp3)", command = changeDownladType)
#        print("downloading audio mode ON (mp3)")
#        
#    if currentMode == 5:
#        resetValues(dt)
#        dt.download_mp3_audio_playlist = 1 
#        ButtonAudioVideoDownloadChange.configure(text="5/12 Now you will download audio PLAYLIST (mp3)", command = changeDownladType)
#        print("downloading audio PLAYLIST mode ON (mp3)")        
#
#    if currentMode == 6:
#        resetValues(dt)
#        dt.download_mp4_audio = 1
#        ButtonAudioVideoDownloadChange.configure(text="6/12 Now you will download audio (mp4)", command = changeDownladType)
#        print("downloading audio mode ON (mp4)")
#
#    if currentMode == 7: 
#        resetValues(dt)
#        dt.download_mp4_audio_playlist = 1
#        ButtonAudioVideoDownloadChange.configure(text="7/12 Now you will download audio PLAYLIST (mp4)", command = changeDownladType)
#        print("downloading audio playlist mode ON (mp4)")
#
#    if currentMode == 8: 
#        resetValues(dt)
#        dt.download_video_playlist_720pMAX = 1 
#        ButtonAudioVideoDownloadChange.configure(text="8/12 Now you will download vido PLAYLIST (720p MAX)", command = changeDownladType)
#        print("downloading video playlist in high quality mode ON (720p MAX)")
#
#    if currentMode == 9:
#        resetValues(dt)
#        dt.download_video_1080p_merge = 1
#        ButtonAudioVideoDownloadChange.configure(text="9/12 download video 1080p and merge with audio",command = changeDownladType)
#        label_download.configure(background="White" , text = "Warning, energy consuming! " ,fg=TEXT_warning)
#        print("downloading video 1080p + merge with audio mode ON (WARNING: Energy consuming!)")  
#    
#    if currentMode == 10:
#        resetValues(dt)
#        dt.download_video_1080p = 1
#        ButtonAudioVideoDownloadChange.configure(text="10/12 Now you will download video in 1080p with no Voice", command = changeDownladType)
#        print("downloading video 1080p ON (mp4, no sound)")     
#
#    if currentMode == 11:
#        resetValues(dt)
#        dt.download_video_LQ = 1
#        ButtonAudioVideoDownloadChange.configure(text="11/12 Now you will download video (Lowest quality)", command = changeDownladType)
#        print("downlading video mode ON (Lowest Quality)")
#
#    if currentMode == 12: 
#        resetValues(dt)
#        dt.download_video_playlist_LQ = 1
#        ButtonAudioVideoDownloadChange.configure(text="12/12 Now you will download video PLAYLIST (lowest quality)", command = changeDownladType)
#        print("downloading video playlist in ON (Lowest Quality)")
#    
#    currentMode += 1 
#    if currentMode >= max_modes:
#        currentMode = 1 

# Top level window
frame = tkinter.Tk()
frame.title("YouTube Audio / Video Downloader")
frame.geometry('500x350')
frame.configure(background=ASCI_grey)

myFont = font.Font(family='Helvetica', size=12)

global SAVE_PATH
SAVE_PATH = ""
global link 
link = ""

def enableDownloadButton():
    if ButtonDownload["state"] == "disabled":
        ButtonDownload["state"] = "normal" #other options: active

def buttonActionConfirmThePath():
    global SAVE_PATH
    SAVE_PATH = textBoxPath.get(1.0, "end-1c")
    SAVE_PATH = change_backslashes(SAVE_PATH)
    labelPath.config(text = "Provided Input: "+SAVE_PATH)
    enableDownloadButton()
    
#def buttonActionDownload():
#    global SAVE_PATH
#    global link 
#    link = textBoxDownload.get(1.0, "end-1c")
#    label_download.config(text = "Provided Input: "+link)  
#    print("Try download a video\nlink: ",link,"\nSAVE_PATH:",SAVE_PATH)
#    print(dt.download_video_720pMAX,
#          " ",dt.download_video_LQ,
#          " ",dt.download_mp4_audio,
#          " ",dt.download_mp4_audio_playlist,
#          " ",dt.download_video_playlist_720pMAX,
#          " ",dt.download_video_playlist_LQ,
#          " ",dt.download_video_1080p,
#          " ",dt.download_mp3_audio,
#          " ",dt.download_mp3_audio_playlist,
#          " ",dt.download_video_1080p_merge,
#          " ",dt.download_mp3_audio_with_thumbnail,
#          " ",dt.download_mp3_audio_playlist_with_thumbnails)
#
#    if dt.download_video_720pMAX == 1:
#        download_video_720pMAX_f(link,SAVE_PATH)
#    
#    if dt.download_video_LQ == 1:
#        download_video_LQ_f(link,SAVE_PATH)
#    
#    if dt.download_mp4_audio == 1:
#        download_mp4_audio_f(link,SAVE_PATH)
#    
#    if dt.download_mp4_audio_playlist == 1:
#        download_mp4_audio_playlist_f(link,SAVE_PATH)
#    
#    if dt.download_video_playlist_720pMAX == 1:
#        download_video_playlist_720pMAX_f(link,SAVE_PATH) 
#
#    if dt.download_video_playlist_LQ == 1:
#        download_video_playlist_LQ_f(link,SAVE_PATH)        
#    
#    if dt.download_video_1080p == 1:
#        link = playlistOrNot(link,"single_video")
#        downloadVideoWithRezolution(SAVE_PATH,link,"1080p") # other: 1440p , 2160p
#            
#    if dt.download_mp3_audio == 1:
#        download_mp3_audio_f(link,SAVE_PATH)
#        
#    if dt.download_mp3_audio_with_thumbnail == 1: 
#        download_mp3_audio_with_thumbnail_f(link,SAVE_PATH)  
# 
#    if dt.download_mp3_audio_playlist == 1:
#        download_mp3_audio_playlist_f(link,SAVE_PATH)
#              
#    if dt.download_mp3_audio_playlist_with_thumbnails == 1:
#        download_mp3_audio_playlist_with_thumbnails_f(link,SAVE_PATH)      
#        
#    if dt.download_video_1080p_merge == 1:
#        downloadVideo_1080p()
#        downloadAudioToBeMerged()
#        merge_video_with_audio() 
#
#    print(time_now(),' Finished working!') 

def startDownloading():
    global link 
    global SAVE_PATH
    link = textBoxDownload.get(1.0, "end-1c")
    label_download.config(text = "Provided Input: "+link)  
    chosen_plan = cmb.get()
    print("Try download a video\nlink: ",link,"\nSAVE_PATH:",SAVE_PATH)
    
    if chosen_plan == "video 720p MAX":
        download_video_720pMAX_f(link,SAVE_PATH)
            
    if chosen_plan == "audio mp3 with thumbnail":
        download_mp3_audio_with_thumbnail_f(link,SAVE_PATH) 
        
    if chosen_plan == "audio mp3 playlist with thumbnails":
        download_mp3_audio_playlist_with_thumbnails_f(link,SAVE_PATH) 
         
    if chosen_plan == "audio mp3":
        download_mp3_audio_f(link,SAVE_PATH)
         
    if chosen_plan == "audio playlist mp3":
         download_mp3_audio_playlist_f(link,SAVE_PATH)
         
    if chosen_plan == "audio mp4":
         download_mp4_audio_f(link,SAVE_PATH)
         
    if chosen_plan == "audio playlist mp4":
        download_mp4_audio_playlist_f(link,SAVE_PATH)
         
    if chosen_plan == "video playlist 720p MAX":
        download_video_playlist_720pMAX_f(link,SAVE_PATH)
        
    if chosen_plan == "video 1080p and merge with audio":
        downloadVideo_1080p_toBeMerged(link,SAVE_PATH)
        downloadAudioToBeMerged(link,SAVE_PATH)
        merge_video_with_audio()
       
    if chosen_plan == "video in 1080p with no Voice":
        downloadVideoWithRezolution(SAVE_PATH,link,"1080p") # other: 1440p , 2160p
        
    if chosen_plan == "video (Lowest quality)":
        download_video_LQ_f(link,SAVE_PATH)
        
    if chosen_plan == "video playlist (Lowest quality)":
        download_video_playlist_LQ_f(link,SAVE_PATH) 

#def browse(): # not working 
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

#now =  datetime.now()
#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#date_time = stringReplace(date_time,'/','-') 
#date_time = stringReplace(date_time,':','-')+'.3gpp'
#date_time = date_time[:-5]
#print(date_time)

print(time_now())


# textbox for the path ----------------------

textBoxPath = tkinter.Text(frame,height = 5,width = 20) # TextBox Creation
textBoxPath.pack()

# Label with info <enetering the path> ------

labelPath = tkinter.Label(frame, text = "Enter here^ a PATH where to download:^",background=ASCI_grey,fg=TEXT_collor)
labelPath['font'] = myFont
labelPath.pack()

# Button Creation

# Button to confirm tha path ----------------

ButtonPathConfirm = tkinter.Button(frame,text = "confirm the PATH", command = buttonActionConfirmThePath)
ButtonPathConfirm['font'] = myFont
ButtonPathConfirm.pack()
# Label Creation
#browse_B = tkinter.Button(frame,text="Browse",command=Browse,width=10,bg="bisque",relief=GROOVE)
#browse_B.pack()
#browse_B.grid(row=3,
#              column=2,
#              pady=1,
#              padx=1)

# Browse Button TODO -----------------------

#browseButton = tkinter.Button(frame,text="browse",command=browse)
#browseButton.pack()

# Textbox for the link ----------------------

textBoxDownload = tkinter.Text(frame,height = 5,width = 20)  
textBoxDownload.pack()

# Label with info for the <confirm the path>

label_download = tkinter.Label(frame,text="Enter here a YouTube Link ^", background=ASCI_grey,fg=TEXT_collor)
label_download['font'] = myFont
label_download.pack()

# Button to confirm download ----------------

ButtonDownload = tkinter.Button(frame,text = "confirm link and download", command = startDownloading ) #buttonActionDownload
ButtonDownload.pack()
ButtonDownload["state"] = "disabled"  # button is disabled at start 
ButtonDownload['font'] = myFont

# Combobox ------------------------

dtt = downloadType
cmb=ttk.Combobox(frame,values=dtt.course,width=30,state = "readonly",font=myFont)
cmb.current(0) # show first option 
frame.option_add('*TCombobox*Listbox.font', myFont) # apply font to combobox list
cmb.pack()

# audio / video change button ----------------

#dt = DonwnloadType 
#
#temp_string = ""
#if dt.download_video_720pMAX == 1:
#    temp_string = "video (720p max)"
#if dt.download_video_LQ == 1:
#    temp_string = "video (Lowest Quality)"
#if dt.download_mp4_audio == 1:
#    temp_string = "audio (mp4)"   
#
#ButtonAudioVideoDownloadChange = tkinter.Button(frame,text="1/12 Now you will download "+temp_string, command = changeDownladType)
#ButtonAudioVideoDownloadChange['font'] = myFont
#ButtonAudioVideoDownloadChange.pack()

# Download Button ----------------

#ButtonDownload = tkinter.Button(frame, text="Download", command = startDownloading)
#ButtonDownload['font'] = myFont
#ButtonDownload.pack()

# Label with info for the button above ------

#label_audioVideoChange = tkinter.Label(frame,text="You can change wether you want do download video / audio ^", background=ASCI_grey,fg=TEXT_collor)
#label_audioVideoChange['font'] = myFont
#label_audioVideoChange.pack()

frame.mainloop()
