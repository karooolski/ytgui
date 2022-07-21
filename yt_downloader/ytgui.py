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
#https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/

global download_audio
global download_audio_playlist 
global download_video_HQ
global download_video_LQ
global download_video_playlist_HQ
global download_video_playlist_LQ
global currentMode
currentMode = 2

download_video_HQ = 1 
download_video_LQ = 0
download_audio = 0 
download_audio_playlist = 0
download_video_playlist_HQ = 0 
download_video_playlist_LQ = 0

# def step():
#     for i in range(5):
#         ws.update_idletasks()
#         pb1['value'] += 20
#         time.sleep(1)

#def temp_text(e):
#   textBoxPath.delete(0,"end")

ASCI_grey = "#808080"
TEXT_collor = "white"

def playlistOrNot(linkk,confirm):
    if link.__contains__('https://www.youtube.com/playlist?list=') and confirm == "playlist":
        return link
    if not (linkk.__contains__('https://www.youtube.com/playlist?list=')) and confirm == "single_video":
        return link
    else:
        print("UserErorr: link adressing playlist, not one film")
        return ' ' # https://www.youtube.com/watch?v=uXKdU_Nm-Kk

def changeDownladType():
    global download_audio 
    global download_audio_playlist 
    global download_video_HQ
    global download_video_LQ
    global download_video_playlist_HQ
    global download_video_playlist_LQ   
    global currentMode 

    if currentMode == 1:
        download_video_HQ = 1 
        download_video_LQ = 0
        download_audio = 0
        download_audio_playlist = 0
        download_video_playlist_HQ = 0 
        download_video_playlist_LQ = 0
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video (High quality)", command = changeDownladType)
        print("downlading video mode ON (HQ)")
    if currentMode == 2:
        download_video_HQ = 0
        download_video_LQ = 1
        download_audio = 0
        download_audio_playlist = 0
        download_video_playlist_HQ = 0 
        download_video_playlist_LQ = 0
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video (Low quality)", command = changeDownladType)
        print("downlading video mode ON (LQ)")
    if currentMode == 3:
        download_video_HQ = 0
        download_video_LQ = 0
        download_audio = 1
        download_audio_playlist = 0
        download_video_playlist_HQ = 0 
        download_video_playlist_LQ = 0
        ButtonAudioVideoDownloadChange.configure(text="Now you will download audio ", command = changeDownladType)
        print("downloading audio mode ON")
    if currentMode == 4: 
        download_video_HQ = 0
        download_video_LQ = 0
        download_audio = 0
        download_audio_playlist = 0
        download_audio_playlist = 1
        download_video_playlist_HQ = 0 
        download_video_playlist_LQ = 0
        ButtonAudioVideoDownloadChange.configure(text="Now you will download audio PLAYLIST", command = changeDownladType)
        print("downloading audio playlist mode ON")

    if currentMode == 5: 
        download_video_HQ = 0
        download_video_LQ = 0
        download_audio = 0
        download_audio_playlist = 0
        download_audio_playlist = 0
        download_video_playlist_HQ = 1 
        download_video_playlist_LQ = 0
        ButtonAudioVideoDownloadChange.configure(text="Now you will download vido PLAYLIST (HQ)", command = changeDownladType)
        print("downloading video playlist in high quality mode ON")

    if currentMode == 6: 
        download_video_HQ = 0
        download_video_LQ = 0
        download_audio = 0
        download_audio_playlist = 0
        download_audio_playlist = 0
        download_video_playlist_HQ = 0 
        download_video_playlist_LQ = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video PLAYLIST (LQ)", command = changeDownladType)
        print("downloading video playlist in low quality mode ON")
        
    currentMode += 1 
    if currentMode >= 7:
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
    global download_video_HQ
    global download_video_LQ
    global download_audio
    global download_audio_playlist
    global download_video_playlist_HQ
    global download_video_playlist_LQ

    print(download_video_HQ," ",download_video_LQ," ",download_audio," ",download_audio_playlist," ",download_video_playlist_HQ," ",download_video_playlist_LQ)

    if download_video_HQ == 1:
        link = playlistOrNot(link,"single_video")
        try: 
            yt = YouTube(link,on_progress_callback=on_progress) 
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)    
        except: 
            print("download_video_HQ error!\n Do you set the PATH correctly?")
    if download_video_LQ == 1:
        link = playlistOrNot(link,"single_video")
        try:
            yt = YouTube(link,on_progress_callback=on_progress)
            stream = yt.streams.first()
            stream.download(SAVE_PATH)
        except:
            print("download_video_LQ: error!")
    if download_audio == 1:
        link = playlistOrNot(link,"single_video")
        try:
            yt = YouTube(link,on_progress_callback=on_progress)
            yt.streams.get_audio_only("mp4").download(SAVE_PATH)
        except:
            print("yt.streams.get_audio_only: error!")
    if download_audio_playlist == 1:
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
                    #yt2.video.streams.filter(only_audio=True).first().download(SAVE_PATH)
                    try:
                        yt.streams.get_audio_only("mp4").download(SAVE_PATH)
                    except: print("download_audio_playlist: Stream download erorrrrrrr")
                    count_ += 1
                except:
                    print("some problem occured during dowloading!")
        except:
            print("Erorr during downloading palylist")
            print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")
    
    if download_video_playlist_HQ == 1:
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
                    print("download_video_playlist_HQ: fail during downloading")
        except:
            print("download_video_playlist_HQ: error!")    

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
                    print("download_video_playlist_HQ: fail during downloading")
        except:
            print("download_video_playlist_HQ: error!")          
                
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
if download_video_HQ == 1:
    temp_string = "video (High Quality)"
if download_video_LQ == 1:
    temp_string = "video (Low Quality)"
if download_audio == 1:
    temp_string = "audio"   



ButtonAudioVideoDownloadChange = tkinter.Button(frame,text="Now you will download "+temp_string, command = changeDownladType)
ButtonAudioVideoDownloadChange['font'] = myFont
ButtonAudioVideoDownloadChange.pack()
label_audioVideoChange = tkinter.Label(frame,text="You can change wether you want do download video / audio ^", background=ASCI_grey,fg=TEXT_collor)
label_audioVideoChange['font'] = myFont
label_audioVideoChange.pack()

frame.mainloop()
