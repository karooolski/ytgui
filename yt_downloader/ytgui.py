# GUI -------------------------------------
import tkinter
from tkinter import ttk
from tkinter import messagebox as msg

from tkinter import filedialog # for browse button, 
# if you have google drive file stream isntalled on your PC it may output  
# <DATE> [17452:ShellIpcClient] shell_ipc_client.cc:129:Connect Can't connect to socket at: \\.\Pipe\GoogleDriveFSPipe_<USER>_shell
# during browsing files, for now I dont know how to surpass it in safe way 
# the same output is being produced during using alternative filedialog from PySimpleGUI lib
 
import tkinter.font as font
# PYTUBE API ------------------------------
from pytube import Playlist
from pytube import YouTube 
#from pytube.cli import on_progress #this module contains the built in progress bar. (console)
#from pytube import Channel
# System -------------------------------------------------
import os
from datetime import datetime
import time # sleep
import requests
# System :: If file exists etc-------------------------------
import os.path
#from os.path import exists
# import atexit # System :: making before exit action (saving log)
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

import threading
#import multiprocessing
import sys
import urllib.request # check internet connection
#from canvas import *
from sqlitedict import SqliteDict # simple database for storing user options locally: -----------------

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
        #"videos : whole channel 720p MAX"
    ]

# # GUI     
#---------------

ASCI_grey = "#808080"
dark_cyan = "#308080"
light_blue = "#00fdec"
main_collor = "black"
TEXT_collor = "white"
TEXT_warning = "red"
gui_font = 'Helvetica'
gui_font_size = 15
frame_title = "ytgui : YouTube Audio / Video Downloader"
frame_geometry="504x510"
version = "1.0.13"
        
# # DEBUG : 
#---------------
class Debug:
    make_logs = False
    show_cmd_details = False
    append_debug_details_to_logs = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class UserConfig():
    link  = ""
    SAVE_PATH = " "
    allow_logs = False
    details_in_cmd  = False
    details_in_loggs  = False
    last_combobox_state = 0
    
    # default configuration
    def __init__(self):
        self.link = ""
        self.SAVE_PATH = ""
        self.allow_logs=False
        self.details_in_cmd=False
        self.details_in_loggs=False
        self.last_combobox_state = 0

    #@staticmethod
    def saveConfiguration(self,key, value):             # save object with user configuration to existing cache file
        cache_file="cache.sqlite3"
        try:
            with SqliteDict(cache_file) as mydict:
                mydict[key] = value # Using dict[key] to store
                mydict.commit() # Need to commit() to actually flush the data
        except Exception as ex:
            print("Error during storing data (Possibly unsupported):", ex)

    #@staticmethod
    def loadConfiguration(self,key):
        cache_file="cache.sqlite3"
        try:
            with SqliteDict(cache_file) as mydict:
                object_ = mydict[key] # No need to use commit(), since we are only loading data!
            return object_
        except Exception as ex:
            debuglog("Creating new user configuration file :")
            object_ = UserConfig()  # make new default config file if it didnt exist
            object_.saveConfiguration(key,object_)
            return object_ #mydict[key]

    def returnDetailsInLogs(self):
        return self.details_in_loggs

# two methods from pytube.cli: TODO merge with tkinter GUI progressbar 
import shutil
def display_progress_bar(
    bytes_received: int, filesize: int, ch: str = "█", scale: float = 0.55
) -> None:
    """Display a simple, pretty progress bar.

    Example:
    ~~~~~~~~
    PSY - GANGNAM STYLE(강남스타일) MV.mp4
    ↳ |███████████████████████████████████████| 100.0%

    :param int bytes_received:
        The delta between the total file size (bytes) and bytes already
        written to disk.
    :param int filesize:
        File size of the media stream in bytes.
    :param str ch:
        Character to use for presenting progress segment.
    :param float scale:
        Scale multiplier to reduce progress bar size.

    """
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = f" ↳ |{progress_bar}| {percent}%\r"
    sys.stdout.write(text)
    sys.stdout.flush()

from pytube import Stream
from pytube.cli import display_progress_bar
@staticmethod
def on_progress(
    stream: Stream, chunk: bytes, bytes_remaining: int
) -> None:  # pylint: disable=W0613
    filesize = stream.filesize
    #print("stream.filesize = "+str(filesize))
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)
       

# # Download Functions : Audios 
# -----------------------------

def download_mp3_audio_with_thumbnail(link : str,SAVE_PATH : str):
    log("download_mp3_audio_with_thumbnail()\nDownloading started "+time_now()+"\n---------------------------------------")
    if ( validLink(link,"single_video") == False):
        return 
    
    yt = YouTube(link,on_progress_callback=on_progress)

    try:
        print_info_downloading_single_file(yt.title,link)
        
        if fileExsists(SAVE_PATH,yt.title,link):
            log("----File is already exists!---")
            msg.showinfo(title="information", message="File is already exists in current path")
            return 
         
        audio = download_audio(yt, SAVE_PATH)
        file_path = ""
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            errorLog("Error: download_mp3_audio_with_thumbnail():couldn`t convert mp4 to mp3")
        set_meta_data(yt, SAVE_PATH, file_path , link, "single_video" , "None" )
        
        try:
            files_links.append(link) # can be helpful if there are duplicates in playlist
            files_names.append(yt.title+".mp3")
        except:
            log("Erorr: download_mp3_audio_with_thumbnail(): cant append downloaded data do list ")   
    except:
        errorLog("download_mp3_audio_with_thumbnail: whole function send error message!")    

def download_mp4_audio(link,SAVE_PATH):
    log("download_mp4_audio()\nDownloading started "+time_now()+"\n---------------------------------------")
    if ( validLink(link,"single_video") == False):
        return 
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title,link)
        yt.streams.get_audio_only("mp4").download(SAVE_PATH)
    except:
        errorLog("yt.streams.get_audio_only: error!")

# Usage: download video in 1080p and merge with audio
def downloadAudioToBeMerged(link,SAVE_PATH):   #download audio onldy
    global title       # variable for merge and rename purposes
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title,link)
        #yt.streams.filter(abr="160kbps", progressive=False).first().download(SAVE_PATH,filename="audiocbd")
        yt.streams.get_audio_only("mp4").download(SAVE_PATH,filename="audiomerge.mp4")
        title = yt.title
        return True
    except: 
        errorLog("Error: downloadAudioToBeMerged(): Download audio failed")
        return False

def download_mp3_audio(link,SAVE_PATH):
    log("download_mp3_audio()\nDownloading started "+time_now()+"\n---------------------------------------")
    if ( validLink(link,"single_video") == False):
        return 
    yt = YouTube(link,on_progress_callback=on_progress)
    if yt == False:
        return
    print_info_downloading_single_file(yt.title,link)
    try:
        audio = download_audio(yt, SAVE_PATH)
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            errorLog("Error: download_mp3_audio(): couldnt convert mp4 to mp3")
    except:
        errorLog("Error download_mp3_audio(): audio mp3 dowloading error!")


# # Download Functions : Videos
# -----------------------------

# Usage: download video in 1080p and merge with audio
def downloadVideo_1080p_toBeMerged(link,SAVE_PATH):   #download video only
    log("downloadVideo_1080p_toBeMerged\nDownloading started "+time_now()+"\n---------------------------------------")
    try:  
        yt = YouTube(link,on_progress_callback=on_progress)
        if yt == False: 
            return 
        try: 
            print_info_downloading_single_file(yt.title,link)
        except: pass
        yt.streams.filter(res="1080p", progressive=False).first().download(SAVE_PATH,filename="videomerge.mp4")
        return True
    except:
        errorLog("Error: downloadVideo_1080p_toBeMerged(): Download video failed")
        return False    

# usage: downloading mp3 , # inner function for other functions
def download_audio(_yt_: YouTube, save_path: str):
    print("download_audio: save path = " + save_path)
    debuglog("yt: " + str(_yt_))
    try:
        #print_info_downloading_single_file(_yt_.title) # errors
        #audio = _yt_.streams.filter(only_audio=True).get_audio_only() # it is mp4 too # downloads audio slowly, meta_data: editable
        
        try:
            _audio_ = _yt_.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            _audio_.download(save_path)
            print("output audio : "+str ( _audio_ ))
        except:                                                                 # except occures during testing by using outer file
            if(is_internet_connection):
                errorLog("download_audio(): problem occured, retry download")
                download_audio(_yt_,save_path)
        
        #audio = _yt_.streams.filter(subtype="mp4", progressive=True).order_by("abr").last()
            # those 2 above are better becaouse 
            # + progressbar collback works during downloading : 
            # + download is way faster
            # + file is lighter (~(-1KB))
            # info: downlaods video+audio in .mp4 fotmat, meta_data: editable, convertable to .mp3
        
        #audio.download(save_path)
        debuglog("download_audio(): end")
        return _audio_ # returning audiofile (mp4) to be converted to mp3 
    except: 
        errorLog("Error: download_audio(): download video (function) error!")

def download_video_720pMAX(link,SAVE_PATH):
    log("download_video_720pMAX()\nDownloading started "+time_now()+"\n---------------------------------------")
    if ( validLink(link,"single_video") == False):
        return 
    try: 
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title,link) 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH) 
    except: 
        errorLog("Error: download_video_720pMAX(): \n Did you set the PATH correctly? , PATH: "+SAVE_PATH)

def download_video_LQ(link,SAVE_PATH):
    log("download_video_LQ\nDownloading started "+time_now()+"\n---------------------------------------")
    if ( validLink(link,"single_video") == False):
        return 
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title)
        stream = yt.streams.first()
        stream.download(SAVE_PATH)
    except:
        errorLog("download_video_LQ: error!")

def downloadVideoWithRezolution(SAVE_PATH,link,rezolution):
    try:
        yt = YouTube(link,on_progress_callback=on_progress) 
        print_info_downloading_single_file(yt.title,link)
        yt.streams.filter(res=rezolution, progressive=False).first().download(SAVE_PATH)
    except: 
        errorLog("Download video in "+str(rezolution)+"p failed")

# # Download Functions : Playlists : Videos
# -----------------------------------------

def download_video_playlist_720pMAX(link,SAVE_PATH):
    log("download_video_playlist_720pMAX()\nDownloading started "+time_now()+"\n---------------------------------------")
    if ( validLink(link,"playlist") == False ):
        return
    #total = 0
    #try:
    #    playlist = Playlist(link)
    #    for video in playlist.videos:
    #        total += 1
    #except:
    #    errorLog("download_video_playlist_720pMAX: ")
    try:
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),total,video.title,temp_link)
                #print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
                count_ += 1
            except:
                errorLog("download_video_playlist_720pMAX: fail during downloading, does video has age restictions?")
    except:
        errorLog("download_video_playlist_720pMAX: error!")  

def download_video_playlist_LQ(link,SAVE_PATH):
    log("download_video_playlist_LQ()\nDownloading started "+time_now()+"\n---------------------------------------")
    if ( validLink(link,"playlist") == False ):
        return
    try:
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),total,video.title,temp_link)
                #print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
                stream = yt.streams.first()
                stream.download(SAVE_PATH)
                count_ += 1
            except:
                errorLog("download_video_playlist_720pMAX: fail during downloading")
    except:
        errorLog("download_video_playlist_720pMAX: error!")  

# # Download Functions : Playlists : Audios
#------------------------------------------

def download_mp3_audio_playlist_with_thumbnails(link : str,SAVE_PATH : str):
    #global link ; global SAVE_PATH
    #link = link ; SAVE_PATH = SAVE_PATH
    log("download_mp3_audio_playlist_with_thumbnails()")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    problem_occured_during_downloading = False
    file_exists_flag = False
    
    if ( validLink(link,"playlist") == False ):
            errorLog("download_mp3_audio_playlist_with_thumbnails : unvalid link")
            return
    
    debuglog("download_mp3_audio_playlist_with_thumbnails(): \n SAVE_PATH = "+SAVE_PATH+"\n link = "+link)
    debuglog("collecting number of videos to download ...")
    
    # get exact value of videos in playlist, because playlist.length also counts unvailable videos
    total = 0
    try:
        playlist = Playlist(link)
        total = str(len(playlist.videos))
        total_ppl = str(playlist.length)
        debuglog("counted total: "+ str(total) + ", playlist length with unvailable videos: " + str(total_ppl) )
    except:
        errorLog("Error : couldnt get max count ")
    debuglog("collecting download data ended, starting connecting to the playlist")
    
    
    # downloading 
    try:
        playlist = Playlist(link)
        count_ = 1
        try:
            for video in playlist.videos:
                temp_link = video.watch_url
                yt = YouTube(temp_link,on_progress_callback=on_progress)    
                file_path = ""
                title = "title"
                # interestingly, assigning a video title to a <string> variable can cause problems (either yt.title and video.title)
                try: title = str(yt.title)    # no errors found if it is like that
                except :
                    try:
                        title = str(video.title)
                    except:
                        title = "<can`t_get_title>"
                try:
                    #vid_title = video.title  
                    #print_info_downloading_playlist(str(count_),total,vid_title,temp_link)
                    inf =  str(time_now()+" downloading ("+str(count_)+"/"+str(total)+") "+title+" "+temp_link)
                    log(inf)
                except: 
                    log("Error: download_mp3_audio_playlist_with_thumbnails(): print info error ")
                try:
                    debuglog("to fileExsists commes:"+" "+SAVE_PATH+" "+title+" "+temp_link)
                    file_exists_flag = False
                    file_exists_flag = fileExsists(SAVE_PATH,title,temp_link)
                    debuglog("---fileExsists(): end() ")
                except: 
                    log(bcolors.WARNING+"Error: "+bcolors.ENDC+"download_mp3_audio_playlist_with_thumbnails: file Exists flag error")
                    log("I'm downloading just in case")
                    file_exists_flag = False # its better to download it if it didnt existeed
                if file_exists_flag == True:
                    count_+=1
                else:    #download: 
                    try:
                        debuglog("--- start downloading")
                        debuglog("yt: " + str(yt))
                        audio = download_audio(yt, SAVE_PATH)
                        file_path = os.path.join(SAVE_PATH,audio.default_filename) # 
                        file_path = convert_to_mp3_with_metadata(file_path)
                        set_meta_data(yt, SAVE_PATH, file_path , temp_link, "playlist" , playlist.title )
                        count_ += 1
                        try:
                            files_links.append(temp_link) # can be helpful if there are duplicates in playlist
                            files_names.append(video.title+".mp3")
                        except:
                            errorLog("Erorr: download_mp3_audio_playlist_with_thumbnails(): cant append downloaded data do list ") 
                    except:
                        errorLog("Error: download_mp3_audio_playlist_with_thumbnails(): some problem occured during dowloading!")
                        problem_occured_during_downloading = True
        except:
            errorLog("Erorr: download_mp3_audio_playlist_with_thumbnails(): main loop error")
           # print("wysylam temp_link do fileExists" + temp_link) 
            
                # fixed: finding duplicate not always works beacause during converting some chars can by cutted of like : // , / , |
           
    except:
        errorLog("download_mp3_audio_playlist_with_thumbnails(): erorr during downloading playlist")
        
    if (problem_occured_during_downloading):
        log("sleep before next download")
        time.sleep(20) # sleep 10 s
        if(is_internet_connection()):
            thread_download() # download again
    
    #print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")     


def download_mp3_audio_playlist(link,SAVE_PATH):
    log("download_mp3_audio_playlist()\nDownloading started "+time_now()+"\n---------------------------------------")
    try:
        if ( validLink(link,"playlist") == False ):
            return
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),total,video.title,temp_link)
                audio = download_audio(yt, SAVE_PATH)
                file_path = os.path.join(SAVE_PATH, audio.default_filename)
                file_path = convert_to_mp3_with_metadata(file_path)
                count_ += 1
            except:
                errorLog("download_mp3_audio_playlist_f(): some problem occured during dowloading!")
    except:
        errorLog("Erorr during downloading palylist")
        errorLog("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")  


def download_mp4_audio_playlist(link,SAVE_PATH):
    log("download_mp4_audio_playlist()\nDownloading started "+time_now()+"\n---------------------------------------")
    try:
        if ( validLink(link,"playlist") == False ):
            return
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),total,video.title,temp_link)
                try:
                    yt.streams.get_audio_only("mp4").download(SAVE_PATH)
                except: log("download_mp4_audio_playlist: Stream download error")
                count_ += 1
            except:
                errorLog("some problem occured during dowloading!")
    except:
        errorLog("Erorr during downloading palylist")
        errorLog("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")

# for now (2023 02 22), pytube doesnt support channels staritng with with @ patterns 
# def download_chanel_720pMAX(link,SAVE_PATH):
#     log("download_chanel_720pMAX():")
#     log("Downloading started "+time_now()+"\n---------------------------------------")
#     print("elo")
#     try:
#         channel = Channel(link)
#         #for video in channel.videos:
#             #print("1")
#             #print(video._title)
#         #    yt = YouTube(video,on_progress_callback=on_progress)
#         #    #print_info_downloading_single_file(yt.title,link) 
#         #    video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH) 
#     except:
#         log("download_chanel_720pMAX: error")

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
        log("Merge ended successfully")
    except:
        errorLog("Error: merge_video_with_audio(): Merge failed")

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
                except: errorLog("couldnt remove mp4 temporary file")
            except: errorLog("couldnt write and close audiofile")
        except: errorLog("couldnt make AdioFileClip")
    except:
        errorLog("convert_to_mp3_with_metadata function error!")


# setting metadata for mp3 file: information , albulm image
def set_meta_data(yt : YouTube , SAVE_PATH : str, file_path : str ,link : str, mode :str , playlist_title : str ):
    # mode : "playlist" during dowloading from playlist or other if downloading single file 
    try:
        yt_image = requests.get(yt.thumbnail_url) # download video thumbnail  
        with open(os.path.join(SAVE_PATH,"thumbnail.jpg"),'wb') as f: 
            f.write(yt_image.content)
            f.close()
        audiofile = eyed3.load(file_path) # convert audio meta data
        if not audiofile.tag:
            audiofile.initTag()   
        tag = id3.Tag()    
        tag.parse(file_path)
        tag.title = yt.title
        tag.artist = yt.author
        tag.artist_url = link
        #tag.audio_source_url  cant be seen in windows10 property, but inside file : yes
        tag._setEncodedBy("ytgui_v"+version)
        if mode == "playlist":
            tag.album = playlist_title
        try:
            tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'thumbnail.jpg'),'rb').read(), 'image/jpeg')
        except:
            errorLog("couldnt make an image by using tag")
        tag.save(version=eyed3.id3.ID3_V2_3) # important if u want to see effect also in windwos media player
        remove_file(SAVE_PATH,"thumbnail.jpg")             
    except:
        errorLog("Couldn`t make an image to file "+file_path)


# # inside functions 
# -------------------

def is_internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

# those lists are used to find whether the file exists or not, searching by name or link for mp3 files 
def fulfill_lists():
    try:    
        if int(files_names.__len__())<1 :
            debuglog("appending infromation to lists")
            try:
                for filename in os.listdir(SAVE_PATH):

                    if filename.__contains__(".mp4") or filename.__contains__(".mp3"):
                       debuglog("appending \""+filename+"\"") 
                       files_names.append(filename)

                    if filename.__contains__(".mp3"):
                         path = os.path.join(SAVE_PATH, filename)
                         path = change_backslashes(path)
                         #audiofile = eyed3.load(path)
                         tag = id3.Tag()
                         tag.parse(path)
                         #if not tag.artist_url == None:
                         debuglog("appending " + str(tag.artist_url) + " for \"" + filename +"\"")
                         files_links.append(str(tag.artist_url))
            except:
                errorLog("cant set tag to array"+filename)  
    except:
        errorLog("fileExsists() error during getting filenames")              
    debuglog("fileExsists() : Setting infromation to lists ended.")

def fileExsists( SAVE_PATH : str, yt_title : str, link_to_video : str):
    debuglog("---fileExsists(): start() ")
    name_exists = False
    link_exists = False
    try:
        debuglog("comparing files links with existing link")
        # compare URL`s` from .mp3 files metadata from SAVE_PATH to video link that can be downloaded  
        for i in range (len(files_links)):
            if files_links[i] == link_to_video:
                debuglog("file exists:(by a link) for "+link_to_video)
                link_exists = True
                break
        
        debuglog("comparing filenames")
        # checking if in SAVE_PATH exists file with the same filename as yt_title    
        file_name = " "
        for i in range (len(files_names)):
            if This_Two_Are_The_Same(files_names[i], yt_title) or files_names[i] == yt_title: #files_names[i] == link_to_video:
                file_name = files_names[i]
                debuglog("file exists:(by tilte) for \""+yt_title+"\"")
                name_exists = True
                break
        # Verdict:         
        if name_exists and link_exists:
            log(bcolors.WARNING+"------File Exists------(by name and link)"+bcolors.ENDC)
            return True
        elif not name_exists and link_exists: # f.ex. renamed arlier .mp3 files witch had the same name as others 
            log("------File Exists------(by link only)")
            return True
        elif not name_exists and not link_exists:
            #log("------File NOT Exists------(at all)")
            return False
        # next attempt: 
        # there can can be a video with the same title but other content -> changing tittle to <title><date>:  
        elif name_exists and not link_exists and not file_name.__contains__(".mp4"):                       
            debuglog("maybe there is audio with the same title but with an other content ...")
            try:
                type = " "
                debuglog("filename: "+str(file_name))
                if file_name.__contains__(".mp4"):
                    type = ".mp4"
                elif file_name.__contains__(".mp3"):
                    type = ".mp3"
                newname = str(str(file_name[:-3])+" "+time_now_clean()+str(type))
                debuglog("newname: "+newname)
                log("fileExsists(): name_exists and link not exists: renaming file")
                os.rename(SAVE_PATH+"/"+file_name,SAVE_PATH+"/"+newname)    # so rename it 
                log("------File NOT Exists but the same name existed earlier------")
                return False                                         # and download file with the same name as one changed above
            except: 
                errorLog("error: fileExsists(): cant rename a file")
                return True # dont download, becaouse it would overwrite file with the other file
        else:
            debuglog("------File NOT Exists------(Not supported case)")
            return True     # case as above 
        
    except: errorLog("cant find anything in arrays or even print them")
    errorLog("------File NOT Exists rare case------")
    return False

# this program also need '/' slashes in the path like in linux instead "\"
def change_backslashes(word):
    if len(word) == 0:
        return ("")
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
    word_ = list(word)
    for i in range(len(word)):
        if word_[i] == toReplace:
            word_[i] = replacement
        output = ''.join(word_)
    return(output)

def time_now():
    now =  datetime.now()
    date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
    date_time = stringReplace(date_time,'/','.')    
    return date_time

def time_now_clean():
    now =  datetime.now()
    date_time = now.strftime("%Y %m %d, %H %M %S")   
    return date_time

# reuturns file name for a log file (current time as a filename)
def log_filename():
    now =  datetime.now()
    date_time = now.strftime("%Y %m %d, %H %M %S")   
    return date_time

def log(infos : str):
    print(infos) # for user during downloading
    try:
        logs.append(remove_non_ascii(infos)+"\n")
    except: print(bcolors.WARNING+"ERORR: log(): adding to logs list error"+bcolors.ENDC)

def errorLog(infos : str):
    print(bcolors.WARNING + infos + bcolors.ENDC) # for user during downloading
    try:
        logs.append(remove_non_ascii(infos)+"\n")
    except: print(bcolors.WARNING+"ERORR: log(): adding to logs list error"+bcolors.ENDC)
    
# dont show log info during downloading in cmd, but store it in log file
def hiddenlog(infos : str):
    try:
        logs.append(remove_non_ascii(infos)+"\n")
    except: print(bcolors.WARNING+"ERORR: hiddenlog(): adding to logs list error"+bcolors.ENDC)

# for additional log infos 
def debuglog(infos : str):
    append = Debug.append_debug_details_to_logs
    show = Debug.show_cmd_details
    if(append and show):
        log(infos)
    elif(append and not show):
        hiddenlog(infos)
    elif(show and not append):
        print("debug: " + infos)

# (debug) print additional information in cmd
# for masive infos  
def detail(*infos):
    if Debug.show_cmd_details == True:
        for info in infos:
            print(info)
    
def make_log(logs:list):
    if Debug.make_logs == False:
        return 
    try:
        logfilename= log_filename()
        file = open("logs/"+logfilename+".txt","w")
        for i in range (len(logs)):
            file.write(str(logs[i]))
        file.close()
    except FileNotFoundError:
        os.makedirs("logs")
        make_log(logs)
    except: 
        errorLog("make_log(): some problem occured!")

def exit_handler(): # TODO it should had been here for saving log file but havent worked yet
    print("test before exit")
    
# old method of saving SAVE_PATH    
# usage: remember last save location (SAVE_PATH)
# update or create file with new content (old content erased)
#def updateFile(filename : str, content : str):
#    try:
#        file = open(filename,"w")
#        file.write(content)
#        file.close()
#    except:
#        errorLog("Erorr: updateFile()")

# usage: remember last save location (SAVE_PATH)    
#def read_file(filename : str):
#    try:
#        file = open(filename, 'r')
#        content = file.read()
#        file.close()
#        return content
#    except FileNotFoundError:
#        updateFile(filename,"set path here")
#        return "set path here"

def print_info_downloading_single_file(video_title : str, video_link : str):
        try:
            info = time_now()+" downloading "+video_title+" "+video_link
            log(info)
        except:
            errorLog("print_info_downloading_single_file(): couldn`t make log")
        
def print_info_downloading_playlist(count_: str, total: str , video_title : str , video_link : str):
    info = "time_info"
    try:
        info = time_now()+" downloading ("+str(count_)+"/"+str(total)+") "+video_title+" "+video_link
        #label_download.configure(text="downloading "+ str(count_) +" from " + str(total))
    except: print("error: print_info_downloading_playlist(): making info error")
    try:
        log(info)
    except: print ("error: print_info_downloading_playlist(): making log error") 

def validLink(link_,confirm):
    print("provided link: "+link_)
    try:
        debuglog("checking playlist or single video and others: ")
        if link_.__contains__('https://www.youtube.com/watch?v=') and link_.__contains__('&list=') and confirm == "single_video":
            debuglog("single_video confirmed inside playlist")
            return True
        if link_.__contains__('https://www.youtube.com/playlist?list=') and confirm == "playlist":
            print("playlist confirmed")
            print("--------------------------------")
            return True
        if not (link_.__contains__('https://www.youtube.com/playlist?list=')) and link_.__contains__("https://www.youtube.com/watch?v=") and confirm == "single_video":
            print("single video confirmed")
            print("--------------------------------")
            return True
        if link_.__contains__('https://www.youtube.com/shorts/') and confirm == "single_video":
            debuglog("downloading short")
            return True
        else:
            msg.showinfo(title="Error", message="UserErorr: Propably you have entered some wrong input, check link and the path")
            print("UserErorr: Propably you have entered some wrong input, check link and the path")
            return False # https://www.youtube.com/watch?v=uXKdU_Nm-Kk
    except: 
        errorLog("Error: validLink(): some problem occured")

def validSavePath(SAVE_PATH : str):
    
    isNotEmpty = False
    isNotSpace = False
    isNotHttps = False
    windows_proper = False
    linux_proper = False
    
    if (not SAVE_PATH == "") : isNotEmpty = True
    if (not SAVE_PATH == " "): isNotSpace = True
    if (not SAVE_PATH.__contains__("https:")) : isNotHttps = True
    if (len(SAVE_PATH) >= 3 and SAVE_PATH.__contains__(":/")) :  windows_proper = True
    if (len(SAVE_PATH) >= 1 and SAVE_PATH.__contains__("/")) : linux_proper = True
    
    if(isNotEmpty and isNotSpace and isNotHttps and windows_proper or linux_proper):
        debuglog("validSavePath: SAVE_PATH is valid")
        enableDownloadButton()
    else :
        disableDownloadButton()
       


# sometimes you want to download a video during watching playlist
# the link contains watch and list in the same but for 
#def singleVideoFromPlaylist():
    
def remove_unnecesary_chars(text : str):
    text = stringReplace(text,".","")
    text = stringReplace(text,",","")
    text = stringReplace(text,"|","")
    text = stringReplace(text,"/","")
    text = stringReplace(text,"`","")
    text = stringReplace(text,"'","")
    text = stringReplace(text,"\"","")
    text = stringReplace(text,":","")
    text = stringReplace(text,"#","")
    text = stringReplace(text,"?","")
    text = stringReplace(text," ","")
    #text = stringReplace(text,"💙","") remove_non_ascii(): doing it 
    #text = stringReplace(text,"🇳🇴","")
    return text

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

# compare two filenames
# taking into account that during download some chacacters can be removed 
def This_Two_Are_The_Same(dir_i_ : str , yt_title_):
    try:
        #debuglog("This_Two_Are_The_Same()?\""+dir_i_+"\" \""+yt_title_+"\"") # massive

        # i want to edit those strings locally so i need to copy it
        dir_i = dir_i_
        yt_title = yt_title_
        
        # dir_i_ has ".mp3" because it is taken from filesystem and yt_title_ doesnt have that: 
        dir_i = dir_i_[:-4] 
        
        # most common case : the names are exacly the same : 
        if dir_i == yt_title:
            debuglog("dir_i == yt_title: \""+dir_i+"\" \""+yt_title+"\"")
            return True

        # case :    "unnecesary chars"
        # the names are the same but downloaded version is without some characters (that happens during download)
        # example : During download "." can be removed as this one:  
        # 
        # downloaded verion  :"CHAINSAW MAN - OP1 - Kick Back (Blinding Sunrise Cover Extended Ver).mp3"
        # yt.title           :"CHAINSAW MAN - OP1 - Kick Back (Blinding Sunrise Cover Extended Ver.).mp3"
        # 
        # And we dont want to donwnload again olny becaouse the name is different 
        # So i am cutting off every character that vanishes after download and comparing names 

        dir_i = remove_unnecesary_chars(dir_i)
        yt_title = remove_unnecesary_chars(yt_title)
        
        if dir_i == yt_title:
            debuglog("dir_i == yt_title: after removed unnecesary chars \""+dir_i+"\" \""+yt_title+"\"")
            return True

        # case : title has other asci characters that can`t be cought by remove_unnecesary_chars()
        
        dir_i = remove_non_ascii(dir_i)
        yt_title = remove_non_ascii(yt_title)

        if dir_i == yt_title and not dir_i == "":
            debuglog("dir_i == yt_title after removed non asci characters: \""+dir_i+"\" \""+yt_title+"\"")
            return True

        # case : if the title consist of only non asci character f.ex chinese/japanese titles
        # then after removal there is nothing to compare, empty string 
    
        if (dir_i == yt_title and dir_i == ""):
            debuglog("(dir_i == yt_title and dir_i ==\"\", nothing here: \""+dir_i+"\" \""+yt_title+"\"")
            # it means remove_non_ascii() remved the whote title (whole title consisted of non asci characters)
            # and can`t compare it`
            return False

        else:
            
            return False
    except:
        errorLog("Error: This_Two_Are_The_Same() ") # massive if True
    
    return False

# # Button Fucntions (Tkinter)  +  Event Actions 
# -----------------------------------------------

def disableDownloadButton():
    ButtonDownload["state"] = "disabled"

def enableDownloadButton():
    if ButtonDownload["state"] == "disabled":
        ButtonDownload["state"] = "normal" #other options: active

def eventAction_confirmThePath(self):
    try: 
        global SAVE_PATH
        SAVE_PATH = textBoxPath.get(1.0, "end-1c")
        #updateFile("last_location.txt",SAVE_PATH)
        SAVE_PATH = change_backslashes(SAVE_PATH)
        #labelPath.config(text = "Provided Input: "+SAVE_PATH)
        debuglog("eventAction_confirmThePath: len(SAVE_PATH)=" + str(len(SAVE_PATH)) + " SAVE_PATH = "+SAVE_PATH)
        validSavePath(SAVE_PATH)
        userConfig.SAVE_PATH = SAVE_PATH
        userConfig.saveConfiguration("userConfig",userConfig)
    except: 
        errorLog("Error: eventAction_confirmThePath()")

# combobox will always save its state when you just choose ann option
def event_combobox_saveStateOnClick(event):
   try:
    combobox_option = event.widget.get()
    combobox_index = 0 
    for i in range (len(DownloadType.downloadTypes)):           # getting current combobox id 
        if DownloadType.downloadTypes[i] == combobox_option:    # interestingly there is no built-in function in tkinter 
            break                                               # to do this for know, 
        else: 
            combobox_index += 1
    currentComboboxID = str(combobox_index)                     # combobox is setted by sgtring id xd
    debuglog("comboboxGetID(): combobox_inxex="+ currentComboboxID + "  event: "+str(combobox_option))
    userConfig.last_combobox_state = currentComboboxID        # combobox.current(id)  id -> (String)
    userConfig.saveConfiguration("userConfig",userConfig)
   except: 
       errorLog("Error: event_combobox_saveStateOnClick(): unexpected problem")
    
def checkBoxAction_makeLogs( var ):
    #global Debug.make_logs
    if int(var) == 1:
        Debug.make_logs = True
        debuglog("checkBoxAction_makeLogs() ->  Debug.make_logs = true")
        userConfig.allow_logs = True
        userConfig.saveConfiguration("userConfig",userConfig)
    elif int(var) == 0:
        Debug.make_logs = False
        debuglog("checkBoxAction_makeLogs() -> Debug.make_logs = false")
        userConfig.allow_logs = False
        userConfig.saveConfiguration("userConfig",userConfig)

def checkBoxAction_makeDetailedLogs( var ):
    #global Debug.append_debug_details_to_logs  
    global userConfig
    if int(var) == 1:
        Debug.append_debug_details_to_logs = True
        debuglog("checkBoxAction_makeDetailedLogs() ->  Debug.append_debug_details_to_logs = true")
        userConfig.details_in_loggs = True
        userConfig.saveConfiguration("userConfig",userConfig)
    elif int(var) == 0:
        Debug.append_debug_details_to_logs = False
        debuglog("checkBoxAction_makeDetailedLogs() -> Debug.append_debug_details_to_logs = false")
        userConfig.details_in_loggs = False
        userConfig.saveConfiguration("userConfig",userConfig)
        
def checkBoxAction_cmdDetails (var):
    #global Debug.show_cmd_details  
    global userConfig
    if int(var) == 1:
        Debug.show_cmd_details = True
        debuglog("checkBoxAction_cmdDetails() ->  Debug.show_cmd_details = true")
        userConfig.details_in_cmd = True
        userConfig.saveConfiguration("userConfig",userConfig)
    elif int(var) == 0:
        Debug.show_cmd_details = False
        debuglog("checkBoxAction_cmdDetails() -> Debug.show_cmd_details = false")
        userConfig.details_in_cmd = False
        userConfig.saveConfiguration("userConfig",userConfig)

# prevent tkinter winodw from being freezed during downloading 
# or run multiple downloads at once (mess in logs)
def thread_download():
    global label_download
    if (not is_internet_connection()):
        msg.showinfo(title="information", message="No internet connection detected!")
        return 
    try:
        files_links.clear()
        files_names.clear()
        fulfill_lists()
        try:
            label_download.configure(text="Downloading in progress")
        except:
            pass
        print("********************")
        new_thread = threading.Thread(target=startDownloading).start()
    except: 
        errorLog("Error: thread_download(): some problem occured")

def startDownloading():
    debuglog("startDownloading(): start! ")
    global link
    global SAVE_PATH
    global label_download
    
    link = textBoxDownloadLink.get(1.0, "end-1c")
    #label_download.config(text = "Provided Input: "+link)  
    chosen_plan = Combobox.get()
    #print("Try download a video\nlink: ",link,"\nSAVE_PATH:",SAVE_PATH)
    #print("--------------------------------")
    
    # Saving user options
    
    userConfig.link = link
    combobox_index = 0 
    for i in range (len(DownloadType.downloadTypes)):           # getting current combobox id 
        if DownloadType.downloadTypes[i] == Combobox.get():     # interestingly there is no built-in function in tkinter 
            break                                               # to do this for know, 
        else: 
            combobox_index += 1
    userConfig.last_combobox_state = str(combobox_index)        # combobox.current(id)  id -> (String)
    userConfig.saveConfiguration("userConfig",userConfig)
    
    debuglog("cbbx state: " + str(combobox_index))
    
    if len(link) < 5 :
        
        label_download.configure(text=" ") 
        debuglog("startDownloading(): wrong link length")
        msg.showinfo(title="information", message="Wrong link length") 
        textBoxDownloadLink.delete("1.0","end")
        textBoxDownloadLink.insert("end-1c","")
        userConfig.link = ""
        userConfig.saveConfiguration("userConfig",userConfig)
        return 
    
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
        if (downloadVideo_1080p_toBeMerged(link,SAVE_PATH)):
            if(downloadAudioToBeMerged(link,SAVE_PATH)):
                merge_video_with_audio()
       
    if chosen_plan == "video in 1080p with no Voice":
        downloadVideoWithRezolution(SAVE_PATH,link,"1080p") # other: 1440p , 2160p
        
    if chosen_plan == "video (Lowest quality)":
        download_video_LQ(link,SAVE_PATH)
        
    if chosen_plan == "video playlist (Lowest quality)":
        download_video_playlist_LQ(link,SAVE_PATH) 
    
   # if chosen_plan == "videos : whole channel 720p MAX":
   #     download_chanel_720pMAX(link,SAVE_PATH)
    
    
    #label_download.configure(text=" ") 
    log("Downloading endend "+time_now()+"\n---------------------------------------")
    #downloading_thread.join()
    make_log(logs)
    msg.showinfo(title="information", message="Download ended")     


    
def browse(): 
   global SAVE_PATH
   try: 
       browse_path = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
       SAVE_PATH = browse_path
       SAVE_PATH = change_backslashes(SAVE_PATH) # for windows usage 
       textBoxPath.delete("1.0","end")
       textBoxPath.insert("end-1c",browse_path)
       userConfig.SAVE_PATH = SAVE_PATH
       userConfig.saveConfiguration("userConfig",userConfig)
       validSavePath(SAVE_PATH)
   except:
       errorLog("Error: browse(): anything hasn`t been setted")


       
def callbackFunc(event):        # combobox get event as string : title of combo option
     print(event.widget.get())


# -------|
# # Main |
# -------|

global SAVE_PATH
SAVE_PATH = ""
global link 
link = ""
logs = []
browse_path = ""
files_links = []
files_names = []
currentComboboxID = 0
userConfig = UserConfig()
userConfig = userConfig.loadConfiguration("userConfig")
global label_download
#label_download = tkinter.Label()
#downloading_thread = threading.Thread(target=startDownloading)

def main():
            
    global textBoxPath
    global ButtonDownload
    global labelPath
    global textBoxDownloadLink
    global Combobox
    global userConfig
    global SAVE_PATH
    global threads
    global label_download
    x_pos = 100
    y_pos = 20
    main_collor_ = main_collor
    #userConfig = UserConfig()
    #userConfig = userConfig.loadConfiguration("userConfig")
    print(time_now())
    log("start "+time_now()+"\n")
    
    # Top level window -------------------------

    frame = tkinter.Tk()
    frame.title(frame_title + " " + version)
    frame.geometry(frame_geometry)
    frame.resizable(width=False, height=False)
    
    myFont = font.Font(family=gui_font, size=gui_font_size)
    
    ## Background image 
    
    try:
        img = tkinter.PhotoImage(file="background.png")
        img_label = tkinter.Label(frame,image=img)
        frame.attributes('-alpha',0.8)                              # frame transparency 
        #frame.wm_attributes('-transparentcolor',main_collor)       # even whole frame can be transparent 
        img_label.place(x=0, y=0)
    except:
        errorLog("main(): couldnt`t load background image")
        main_collor_ = dark_cyan
        frame.configure(background=main_collor_)
    
    ## background image secod idea
    
    #frame.wm_attributes("-transparentcolor", 'grey')
    #canv = tkinter.Canvas(frame, width= 1000, height= 1000)
    #canv.create_image(252,253,image=img)  #x,y expands the image size, if range is too big than image is starting moving x:-> / y:down
    #canv.place(x=0,y=0)
    
    # LABELS 
    
    ## Label title ------

    labelPath = tkinter.Label(frame, text = "YTGUI",background=main_collor_,fg=TEXT_collor,font = myFont)
    labelPath.place(x=220,y=50)
    
    ## Label with info <enetering the path> ------

    labelPath = tkinter.Label(frame, text = "Enter here^ a PATH where to download:^",background=main_collor_,fg=TEXT_collor,font = myFont)
    labelPath.place(x=60,y=170)

    ## Label with info for the <confirm the path>

    label_enterLink = tkinter.Label(frame,text="Enter here^ a YouTube Link ^", background=main_collor_,fg=TEXT_collor)
    label_enterLink['font'] = myFont
    label_enterLink.place(x=110,y=258)

    ## canvas labels that are without background 
    
    #canv.create_text(280, 50, text="YTGUI", fill="white", font=('Helvetica 15 bold'))
    #canv.create_text(230, 170, text="Enter here^ a PATH where to download:^", fill="white", font=('Helvetica 13 bold'))
    #canv.create_text(230, 260, text="Enter here^ a YouTube Link ^", fill="white", font=('Helvetica 13 bold'))

    ## Label with downloading info ---------------
    
    label_download = tkinter.Label(frame,text=" ", background=main_collor_,fg="#1aff1a", font = myFont).place(x=70,y=360) 

    #TEXTBOXES
    
    ## textbox for the path ----------------------

    textBoxPath = tkinter.Text(frame,height = 2,width = 39, font=('Helvetica 12 bold'),foreground="black") # TextBox Creation
    last_location = userConfig.SAVE_PATH
    textBoxPath.insert("end-1c",last_location)
    SAVE_PATH = last_location
    debuglog("main(): SAVE_PATH = "+SAVE_PATH)
    textBoxPath.configure(background="white")
    #frame.event_add("<<Mouse_LeftClick_Action>>", "<Button>") # my own event 
   #textBoxPath.bind("<<Mouse_LeftClick_Action>>",buttonActionConfirmThePath)
    textBoxPath.bind("<KeyRelease>",eventAction_confirmThePath)
    textBoxPath.place(x=60, y=120)

    ## Textbox for the link ----------------------

    textBoxDownloadLink = tkinter.Text(frame,height = 2,width = 39,font=('Helvetica 12 bold'))  
    textBoxDownloadLink.insert("end-1c",userConfig.link)
    textBoxDownloadLink.place(x=60,y=210)
 
    # Buttons 
    
    ## Browse Button -----------------------------

    browseBtn = tkinter.Button(frame,text = "Browse", command = browse, font = myFont).place(x=410,y=120)
 
    ## Button to confirm download ----------------

    ButtonDownload = tkinter.Button(frame,text = "confirm link and download", command = thread_download ) #buttonActionDownload
    
    #ButtonDownload.pack()
    ButtonDownload.place(x=120,y=290)
    ButtonDownload["state"] = "disabled"  # button is disabled at start 
    ButtonDownload['font'] = myFont
    validSavePath(last_location)    # enable dowload_button if there is already exists a path
    # Combobox to choose an option of download---

    # COMBOBOX

    downloadType = DownloadType
    Combobox=ttk.Combobox(frame,values=downloadType.downloadTypes,width=30,state = "readonly",font=myFont)
    try:
        currentComboboxID = str(userConfig.last_combobox_state)
        Combobox.current(currentComboboxID) # show last watched option 
    except:
        log("main(): incorrect comobox current state,\" "+ userConfig.last_combobox_state +" \" problem has been fixed automaticallly") 
        Combobox.current(0) # show first option
    frame.option_add('*TCombobox*Listbox.font', myFont) # apply font to combobox list
    Combobox.bind("<<ComboboxSelected>>", event_combobox_saveStateOnClick) # event listener
    Combobox.place(x=70,y=330)

    # CHECKBOXES
    
    # checkBoxes to make logs -------------------------
     
    var1 = tkinter.IntVar() # if not this, the 2 checkboxes would be touched in 1 click (graphically)
    var2 = tkinter.IntVar()
    var3 = tkinter.IntVar()
    c1 = tkinter.Checkbutton(frame, 
                             text='make logs',
                             variable=var1,
                             onvalue=1,
                             offvalue=0 ,
                             background=main_collor_,
                             fg=TEXT_collor,
                             selectcolor="blue",
                             command=lambda:checkBoxAction_makeLogs(str(var1.get())) )
    c1['font'] = myFont
    if userConfig.allow_logs == True:
        c1.select()
        #global make_logs
        Debug.make_logs = True
    #c1.pack()
    c1.place(x=70,y=410)
    c2 = tkinter.Checkbutton(frame, 
                             text='add debug details to logs',
                             variable=var2, 
                             onvalue=1,
                             offvalue=0, 
                             background=main_collor_,
                             fg=TEXT_collor,
                             selectcolor="blue",
                             command=lambda:checkBoxAction_makeDetailedLogs(str(var2.get())))
    c2['font'] = myFont
    if userConfig.returnDetailsInLogs() == True:
        c2.select()
        #global Debug.append_debug_details_to_logs
        Debug.append_debug_details_to_logs = True
    #c2.pack()
    c2.place(x=70,y=440)
    c3 = tkinter.Checkbutton(frame, 
                         text='show debug details in cmd',
                         variable=var3, 
                         onvalue=1,
                         offvalue=0, 
                         background=main_collor_,
                         fg=TEXT_collor,
                         selectcolor="blue",
                         command=lambda:checkBoxAction_cmdDetails(str(var3.get())))
    c3['font'] = myFont
    if userConfig.details_in_cmd == True:
        c3.select()
        #global Debug.show_cmd_details
        Debug.show_cmd_details = True
    c3.place(x=70, y=470)  #c3.pack()
    
    frame.mainloop()
    
    #if downloading_thread.is_alive():
    #    downloading_thread.join() # wait until thread is executed
    
    return 0
    
#main()



#downloading_process.join()

#atexit.register(exit_handler)
