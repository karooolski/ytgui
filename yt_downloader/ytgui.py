import tkinter
from tkinter import ttk
from turtle import color
import tkinter.font as font
from pytube import Playlist
from pytube import YouTube 
from pytube.cli import on_progress #this module contains the built in progress bar. 
import time
import os
from datetime import datetime
import colorama
from colorama import Fore
import ffmpeg

import requests
import eyed3
from eyed3.id3.frames import ImageFrame
from eyed3.id3 import tag
import eyed3.id3 as id3
##from eyed3.core import Tag
#from moviepy import *
#import eyed3.mp3.Mp3AudioFile #- For mp3 audio files.
#import eyed3.id3.TagFile #- For raw ID3 data files

from moviepy.audio.io import AudioFileClip
from moviepy.audio.AudioClip import *  # write_audiofile
from moviepy.audio.io.AudioFileClip import * # close

#from moviepy.editor import AudioFileClip # pyinstaller zadziala ale nie zrobi mp3
#from moviepy.audio.io import AudioFileClip # earlier: from moviepy.editor import AudioFileClip
#from moviepy import *
#https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/

global download_mp4_audio
global download_mp3_audio
global download_mp3_audio_with_thumbnail
global download_mp3_audio_playlist
global download_mp3_audio_playlist_with_thumbnails
global download_mp4_audio_playlist 
global download_video_1080p
global download_video_1080p_merge  # download audio && video in 1080p and merge it
global download_video_720pMAX
global download_video_LQ
global download_video_playlist_720pMAX
global download_video_playlist_LQ
global currentMode
currentMode = 2

download_video_1080p = 0
download_video_1080p_merge = 0
download_video_720pMAX = 1 
download_video_LQ = 0
download_mp4_audio = 0 
download_mp3_audio = 0
download_mp3_audio_with_thumbnail = 0 
download_mp3_audio_playlist = 0
download_mp3_audio_playlist_with_thumbnails = 0
download_mp4_audio_playlist = 0
download_video_playlist_720pMAX = 0 
download_video_playlist_LQ = 0

ASCI_grey = "#808080"
TEXT_collor = "white"
TEXT_warning = "red"

# Usage: download video in 1080p and merge with audio
def downloadVideo():   #download video only
    try:  
        yt = YouTube(link,on_progress_callback=on_progress)
        yt.streams.filter(res="1080p", progressive=False).first().download(SAVE_PATH,filename="video.mp4")
    except:
        print("Download video failed")    

# Usage: download video in 1080p and merge with audio
def downloadAudio():   #download audio onldy
    global title
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        yt.streams.filter(abr="160kbps", progressive=False).first().download(SAVE_PATH,filename="audio.mp3")
        title = yt.title
    except: 
        print("Download audio failed")

def remove_file(location,filename):
    path = os.path.join(location,filename)
    os.remove(path)
        
# Usage: download video in 1080p and merge with audio
def merge():
    try:
        video = ffmpeg.input("video.mp4")
        audio = ffmpeg.input("audio.mp3")
        ffmpeg.output(audio, video, title+".mp4").run(overwrite_output=True)
        remove_file(SAVE_PATH,"video.mp4")
        remove_file(SAVE_PATH,"audio.mp3")
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

def playlistOrNot(linkk,confirm):
    if link.__contains__('https://www.youtube.com/playlist?list=') and confirm == "playlist":
        return link
    if not (linkk.__contains__('https://www.youtube.com/playlist?list=')) and confirm == "single_video":
        return link
    else:
        print("UserErorr: link adressing playlist, not one film")
        return ' ' # https://www.youtube.com/watch?v=uXKdU_Nm-Kk

def resetValues():
    global download_mp4_audio
    global download_mp3_audio
    global download_mp3_audio_with_thumbnail
    global download_mp3_audio_playlist 
    global download_mp3_audio_playlist_with_thumbnails
    global download_mp4_audio_playlist 
    global download_video_720pMAX
    global download_video_LQ
    global download_video_playlist_720pMAX
    global download_video_playlist_LQ   
    global download_video_1080p
    global download_video_1080p_merge
    download_video_1080p = 0
    download_video_1080p_merge = 0
    download_video_720pMAX = 0 
    download_video_LQ = 0
    download_mp4_audio = 0
    download_mp3_audio = 0
    download_mp3_audio_with_thumbnail = 0
    download_mp3_audio_playlist = 0
    download_mp3_audio_playlist_with_thumbnails = 0
    download_mp4_audio_playlist = 0
    download_video_playlist_720pMAX = 0 
    download_video_playlist_LQ = 0
    label_download.configure(background=ASCI_grey,text="You can change wether you want do download video / audio ^",fg=TEXT_collor)

def changeDownladType():
    global download_mp4_audio
    global download_mp3_audio
    global download_mp3_audio_with_thumbnail
    global download_mp3_audio_playlist 
    global download_mp3_audio_playlist_with_thumbnails
    global download_mp4_audio_playlist 
    global download_video_1080p
    global download_video_1080p_merge
    global download_video_720pMAX
    global download_video_LQ
    global download_video_playlist_720pMAX
    global download_video_playlist_LQ   
    global currentMode 

    if currentMode == 1:
        resetValues()
        download_video_720pMAX = 1 
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video (720p MAX)", command = changeDownladType)
        print("downlading video mode ON (720p MAX)")

    if currentMode == 2:
        resetValues()
        download_mp3_audio_with_thumbnail = 1
        ButtonAudioVideoDownloadChange.configure(text="download audio mp3 with thumbnail",command = changeDownladType)
    
    if currentMode == 3:
        resetValues()
        download_mp3_audio_playlist_with_thumbnails = 1
        ButtonAudioVideoDownloadChange.configure(text="download audio mp3 playlist with thumbnails",command = changeDownladType)

    if currentMode == 4: 
        resetValues()
        download_mp3_audio = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download audio (mp3)", command = changeDownladType)
        print("downloading audio mode ON (mp3)")
        
    if currentMode == 5:
        resetValues()
        download_mp3_audio_playlist = 1 
        ButtonAudioVideoDownloadChange.configure(text="Now you will download audio PLAYLIST (mp3)", command = changeDownladType)
        print("downloading audio PLAYLIST mode ON (mp3)")        

    if currentMode == 6:
        resetValues()
        download_mp4_audio = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download audio (mp4)", command = changeDownladType)
        print("downloading audio mode ON (mp4)")

    if currentMode == 7: 
        resetValues()
        download_mp4_audio_playlist = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download audio PLAYLIST (mp4)", command = changeDownladType)
        print("downloading audio playlist mode ON (mp4)")

    if currentMode == 8: 
        resetValues()
        download_video_playlist_720pMAX = 1 
        ButtonAudioVideoDownloadChange.configure(text="Now you will download vido PLAYLIST (720p MAX)", command = changeDownladType)
        print("downloading video playlist in high quality mode ON (720p MAX)")

    if currentMode == 9:
        resetValues()
        download_video_1080p_merge = 1
        ButtonAudioVideoDownloadChange.configure(text="download video 1080p and merge with audio",command = changeDownladType)
        label_download.configure(background="White" , text = "Warning, energy consuming! " ,fg=TEXT_warning)
        print("downloading video 1080p + merge with audio mode ON (WARNING: Energy consuming!)")  
    
    if currentMode == 10:
        resetValues()
        download_video_1080p = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video in 1080p with no Voice", command = changeDownladType)
        print("downloading video 1080p ON (mp4, no sound)")     

    if currentMode == 11:
        resetValues()
        download_video_LQ = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video (Lowest quality)", command = changeDownladType)
        print("downlading video mode ON (Lowest Quality)")

    if currentMode == 12: 
        resetValues()
        download_video_playlist_LQ = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video PLAYLIST (lowest quality)", command = changeDownladType)
        print("downloading video playlist in ON (Lowest Quality)")
      
    currentMode += 1 
    if currentMode >= 13:
        currentMode = 1 

def enableDownloadButton():
    if printButtonDownload["state"] == "disabled":
        printButtonDownload["state"] = "normal" #active

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


# Top level window
frame = tkinter.Tk()
frame.title("YouTube Audio / Video Downloader")
frame.geometry('500x350')
frame.configure(background=ASCI_grey)

myFont = font.Font(family='Helvetica', size=12)

def downloadVideoWithRezolution(SAVE_PATH,link,rezolution):
    try:
        yt = YouTube(link,on_progress_callback=on_progress) 
        yt.streams.filter(res=rezolution, progressive=False).first().download(SAVE_PATH)
    except: 
        print("Download video in 1080p failed")

global SAVE_PATH
SAVE_PATH = ""
global link 
link = ""

def buttonActionConfirmThePath():
    input = textBoxPath.get(1.0, "end-1c")
    global SAVE_PATH
    SAVE_PATH = input
    SAVE_PATH = change_backslashes(SAVE_PATH)
    labelPath.config(text = "Provided Input: "+input)
    print(input)
    enableDownloadButton()
    
def buttonActionDownload():
    input = textBoxDownload.get(1.0, "end-1c")
    global SAVE_PATH
    global link 
    link = input
    label_download.config(text = "Provided Input: "+input)  
    print(input)
    print("Try download a video")
    print("link: "+link)
    print("SAVE_PATH: "+SAVE_PATH)
   # try: 
    #    yt = YouTube(link,on_progress_callback=on_progress) 
    #except: 
    #    print("YouTube(link) error: Connection Failed") #to handle exception 
    global download_video_1080p
    global download_video_1080p_merge
    global download_video_720pMAX
    global download_video_LQ
    global download_mp4_audio
    global download_mp3_audio_with_thumbnail
    global download_mp3_audio_playlist
    global download_mp3_audio_playlist_with_thumbnails
    global download_mp3_audio
    global download_mp4_audio_playlist
    global download_video_playlist_720pMAX
    global download_video_playlist_LQ

    print(download_video_720pMAX," ",download_video_LQ," ",download_mp4_audio," ",download_mp4_audio_playlist," ",download_video_playlist_720pMAX," ",download_video_playlist_LQ," ",download_video_1080p," ",download_mp3_audio," ",download_mp3_audio_playlist," ", download_video_1080p_merge," ",download_mp3_audio_with_thumbnail," ",download_mp3_audio_playlist_with_thumbnails)

    if download_video_720pMAX == 1:
        link = playlistOrNot(link,"single_video")
        try: 
            yt = YouTube(link,on_progress_callback=on_progress) 
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)    
        except: 
            print("download_video_720pMAX error!\n Do you set the PATH correctly?")
    
    if download_video_LQ == 1:
        link = playlistOrNot(link,"single_video")
        try:
            yt = YouTube(link,on_progress_callback=on_progress)
            stream = yt.streams.first()
            stream.download(SAVE_PATH)
        except:
            print("download_video_LQ: error!")
    
    if download_mp4_audio == 1:
        link = playlistOrNot(link,"single_video")
        try:
            yt = YouTube(link,on_progress_callback=on_progress)
            yt.streams.get_audio_only("mp4").download(SAVE_PATH)
        except:
            print("yt.streams.get_audio_only: error!")
    
    if download_mp4_audio_playlist == 1:
        try:
            link = playlistOrNot(link,"playlist")
            playlist = Playlist(link)
            count_ = 1
            total = str(playlist.length)
            for video in playlist.videos:
                temp_link = video.watch_url
                yt = YouTube(temp_link,on_progress_callback=on_progress)
                try:
                    print("downloading (",str(count_),"/",str(total),") ",video.title)
                    try:
                        yt.streams.get_audio_only("mp4").download(SAVE_PATH)
                    except: print("download_mp4_audio_playlist: Stream download error")
                    count_ += 1
                except:
                    print("some problem occured during dowloading!")
        except:
            print("Erorr during downloading palylist")
            print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")
    
    if download_video_playlist_720pMAX == 1:
        link = playlistOrNot(link,"playlist")
        try:
            playlist = Playlist(link)
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
                    print("download_video_playlist_720pMAX: fail during downloading")
        except:
            print("download_video_playlist_720pMAX: error!")    

    if download_video_playlist_LQ == 1:
        link = playlistOrNot(link,"playlist")
        try:
            playlist = Playlist(link)
            count_ = 1
            total = str(playlist.length)
            for video in playlist.videos:
                temp_link = video.watch_url
                yt = YouTube(temp_link,on_progress_callback=on_progress)
                try:
                    print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
                    stream = yt.streams.first()
                    stream.download(SAVE_PATH)
                    count_ += 1
                except:
                    print("download_video_playlist_720pMAX: fail during downloading")
        except:
            print("download_video_playlist_720pMAX: error!")          
    
    if download_video_1080p == 1:
        link = playlistOrNot(link,"single_video")
        downloadVideoWithRezolution(SAVE_PATH,link,"1080p") # other: 1440p , 2160p
            
    if download_mp3_audio == 1:
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
        
    if download_mp3_audio_with_thumbnail == 1: 
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
                    
                #audiotag = eyed3.core.Tag
                #audiotag.artist = yt.author
                # eyed3 -> id3 -> tag.py
                tag = id3.Tag()
                tag.parse(file_path)
                tag.title = yt.title
                tag.artist = yt.author
                tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'szablon.jpg'),'rb').read(), 'image/jpeg')
                
                # if input os.path.join(SAVE_PATH,"szablon.jpg")
                # instead 'szablon.jpg'
                # then it works in .exe form but not show in windows media player
                
                # this code works the same, for setting image
                #with open("szablon.jpg", "rb") as cover_art:
                #    tag.images.set(3, cover_art.read(), "image/jpeg")
                
                tag.save(version=eyed3.id3.ID3_V2_3)
                
                #audiofile.tag.title = yt.title
                #audiofile.tag.artist = yt._author
                #audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('szablon.jpg','rb').read(), 'image/jpeg')
                #audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
                remove_file(SAVE_PATH,"szablon.jpg")
                # you can see a thumbnail using VLC media player, on windows
            except:
                print("Couldn`t make an image to file "+file_path)
            
        except:
            print("audio mp3 dowloading error!")      
 
    if download_mp3_audio_playlist == 1:
        try:
            link = playlistOrNot(link,"playlist")
            playlist = Playlist(link)
            count_ = 1
            total = str(playlist.length)
            for video in playlist.videos:
                temp_link = video.watch_url
                yt = YouTube(temp_link,on_progress_callback=on_progress)
                try:
                    print("downloading (",str(count_),"/",str(total),") ",video.title)
                    audio = download_video(yt,"mp3", SAVE_PATH)
                    file_path = os.path.join(SAVE_PATH, audio.default_filename)
                    file_path = convert_to_mp3_with_metadata(file_path)
                    count_ += 1
                except:
                    print("some problem occured during dowloading!")
        except:
            print("Erorr during downloading palylist")
            print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")       
              
    if download_mp3_audio_playlist_with_thumbnails == 1:
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
                    print("downloading (",str(count_),"/",str(total),") ",video.title)
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
                    #audiofile.tag.title = yt.title
                    #audiofile.tag.artist = yt._author
                    #audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('szablon.png','rb').read(), 'image/jpeg')
                    #audiofile.tag.save()
                    
                    #file_path = change_backslashes(file_path)
                    
                    tag = ""
                    try: tag = id3.Tag()    
                    except:  print("couldnt make id3.Tag()")
                    
                    try: tag.parse(file_path)
                    except: print("couldnt parse filepath to tag")
                    try:
                        tag.title = yt.title
                    except:
                        print("couldnt switch fileneme of tag")
                    
                    try: 
                        tag.artist = yt.author
                    except: 
                        print("couldnt make artist name")
                    
                    try:
                        tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'szablon.jpg'),'rb').read(), 'image/jpeg')
                    except:
                        print("couldnt make an image by using tag")
                    # this code works the same, for setting image (not after use pyinstaller, coz of string "szablon.png" must be os.path.join(etc...))
                    #try:
                    #    with open(os.path.join(SAVE_PATH,"szablon.jpg"), "rb") as cover_art:
                    #        tag.images.set(3, cover_art.read(), "image/jpeg")
                    #except:
                    #    print("couldnt set an image by alternative method" + file_path)
                     
                    tag.save(version=eyed3.id3.ID3_V2_3) #version=eyed3.id3.ID3_V2_3
                    remove_file(SAVE_PATH,"szablon.jpg")
                    # you can see a thumbnail using VLC media player, on windows                
                except:
                    print("Couldn`t make an image to file "+file_path)
        except:
            print("Erorr during downloading palylist")
            print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")           
    

    if download_video_1080p_merge == 1:
        downloadVideo()
        downloadAudio()
        merge() 
       
    print('Finished working!') 


now =  datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
date_time = stringReplace(date_time,'/','-') 
date_time = stringReplace(date_time,':','-')+'.3gpp'
date_time = date_time[:-5]
print(date_time)

textBoxPath = tkinter.Text(frame,height = 5,width = 20) # TextBox Creation
textBoxPath.pack()
# Button Creation
printButtonPath = tkinter.Button(frame,text = "confirm the PATH", command = buttonActionConfirmThePath)
printButtonPath['font'] = myFont
printButtonPath.pack()
# Label Creation
labelPath = tkinter.Label(frame, text = "Enter here^ a PATH where to download:^",background=ASCI_grey,fg=TEXT_collor)
labelPath['font'] = myFont
labelPath.pack()

textBoxDownload = tkinter.Text(frame,height = 5,width = 20)  
textBoxDownload.pack()
printButtonDownload = tkinter.Button(frame,text = "confirm link and download", command = buttonActionDownload)
printButtonDownload.pack()
printButtonDownload["state"] = "disabled"  # button is disabled at start 
printButtonDownload['font'] = myFont
label_download = tkinter.Label(frame,text="Enter here a YouTube Link ^", background=ASCI_grey,fg=TEXT_collor)
label_download['font'] = myFont
label_download.pack()

# audio / video change button 

temp_string = ""
if download_video_720pMAX == 1:
    temp_string = "video (720p max)"
if download_video_LQ == 1:
    temp_string = "video (Lowest Quality)"
if download_mp4_audio == 1:
    temp_string = "audio (mp4)"   



ButtonAudioVideoDownloadChange = tkinter.Button(frame,text="Now you will download "+temp_string, command = changeDownladType)
ButtonAudioVideoDownloadChange['font'] = myFont
ButtonAudioVideoDownloadChange.pack()
label_audioVideoChange = tkinter.Label(frame,text="You can change wether you want do download video / audio ^", background=ASCI_grey,fg=TEXT_collor)
label_audioVideoChange['font'] = myFont
label_audioVideoChange.pack()

frame.mainloop()
