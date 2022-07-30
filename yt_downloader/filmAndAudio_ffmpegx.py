#This code download the video and the audio from YouTube and converts it to the one video (mp4)
#Using ffmpeg (added to the path in windows global variables)
from pytube import YouTube #29,30.07.2022
from pytube.cli import on_progress
import ffmpeg # it can download 1080p but without sound
SAVE_PATH = "C:/Users/Karol/Desktop/ytgui" # where to save 

link="https://www.youtube.com/watch?v=vTL10Z0VgTU"

global title
title = ""

def downloadVideo():   #download video only
    try:  
        yt = YouTube(link,on_progress_callback=on_progress)
        yt.streams.filter(res="1080p", progressive=False).first().download(SAVE_PATH,filename="video.mp4")
    except:
        print("Download video failed")    

def downloadAudio():   #download audio onldy
    global title
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        yt.streams.filter(abr="160kbps", progressive=False).first().download(SAVE_PATH,filename="audio.mp3")
        title = yt.title
    except: 
        print("Download audio failed")
    
def merge():
    try:
        video = ffmpeg.input("video.mp4")
        audio = ffmpeg.input("audio.mp3")
        ffmpeg.output(audio, video, title+".mp4").run(overwrite_output=True)
    except:
        print("Merge failed")
downloadVideo()
downloadAudio()
merge()

#print("download failed")
