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
from pytube.cli import on_progress #this module contains the built in progress bar. (console)
from pytube import Channel
# System -------------------------------------------------
import os
from datetime import datetime
import time # sleep
import requests
# System :: If file exists etc-------------------------------
import os.path
from os.path import exists
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

import urllib.request # check internet connection

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
main_collor = dark_cyan
TEXT_collor = "white"
TEXT_warning = "red"
gui_font = 'Helvetica'
gui_font_size = 15
frame_title = "ytgui : YouTube Audio / Video Downloader"
frame_geometry="500x510"

# # DEBUG : 
#---------------

make_logs = False
show_cmd_details = False
append_debug_details_to_logs = False
auto_fill_SAVE_PATH = ""
auto_fill_link_field = ""

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


# # Download Functions : Audios 
# -----------------------------

def download_mp3_audio_with_thumbnail(link : str,SAVE_PATH : str):
    log("download_mp3_audio_with_thumbnail()") 
    log("Downloading started "+time_now()+"\n---------------------------------------")
    if ( playlistOrNot(link,"single_video") == False):
        return 
    
    yt = YouTube(link,on_progress_callback=on_progress)

    try:
        print_info_downloading_single_file(yt.title,link)
        
        if fileExsists(SAVE_PATH,yt.title,link):
            log("----File is already exists!---")
            msg.showinfo(title="information", message="File is already exists in current path")
            return 
         
        audio = download_audio(yt,"mp3", SAVE_PATH)
        file_path = ""
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            log("Error: download_mp3_audio_with_thumbnail():couldn`t convert mp4 to mp3")
        set_meta_data(yt, SAVE_PATH, file_path , link, "single_video" , "None" )
        
        try:
            files_links.append(link) # can be helpful if there are duplicates in playlist
            files_names.append(yt.title+".mp3")
        except:
            log("Erorr: download_mp3_audio_with_thumbnail(): cant append downloaded data do list ") 
        
        
    except:
        log("download_mp3_audio_with_thumbnail: whole function send error message!")    

def download_mp4_audio(link,SAVE_PATH):
    log("download_mp4_audio()")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    if ( playlistOrNot(link,"single_video") == False):
        return 
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title,link)
        yt.streams.get_audio_only("mp4").download(SAVE_PATH)
    except:
        log("yt.streams.get_audio_only: error!")

# Usage: download video in 1080p and merge with audio
def downloadAudioToBeMerged(link,SAVE_PATH):   #download audio onldy
    global title       # variable for merge and rename purposes
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title,link)
        #yt.streams.filter(abr="160kbps", progressive=False).first().download(SAVE_PATH,filename="audiocbd")
        yt.streams.get_audio_only("mp4").download(SAVE_PATH,filename="audiomerge.mp4")
        title = yt.title
    except: 
        log("Download audio failed")

def download_mp3_audio(link,SAVE_PATH):
    log("download_mp3_audio")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    if ( playlistOrNot(link,"single_video") == False):
        return 
    yt = YouTube(link,on_progress_callback=on_progress)
    if yt == False:
        return
    print_info_downloading_single_file(yt.title,link)
    try:
        audio = download_audio(yt,"mp3", SAVE_PATH)
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            log("couldnt convert mp4 to mp3")
    except:
        log("audio mp3 dowloading error!")


# # Download Functions : Videos
# -----------------------------

# Usage: download video in 1080p and merge with audio
def downloadVideo_1080p_toBeMerged(link,SAVE_PATH):   #download video only
    log("downloadVideo_1080p_toBeMerged")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    try:  
        yt = YouTube(link,on_progress_callback=on_progress)
        if yt == False: 
            return 
        print_info_downloading_single_file(yt.title,link)
        yt.streams.filter(res="1080p", progressive=False).first().download(SAVE_PATH,filename="videomerge.mp4")
    except:
        log("Download video failed")    

# usage: downloading mp3
# inner function for other functions
def download_audio(yt: YouTube, file_type: str, downloads_path: str):
    try:
        #print_info_downloading_single_file(yt.title)
    # Download a video and debug progress
        if file_type == "mp4":
            audio = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        else:
            audio = yt.streams.filter(only_audio=True).get_audio_only() # it is mp4 too
        audio.download(downloads_path)
        return audio # returning audiofile (mp4) to be converted to mp3 
    except: 
        log("download video (function) error!")

def download_video_720pMAX(link,SAVE_PATH):
    log("download_video_720pMAX()")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    if ( playlistOrNot(link,"single_video") == False):
        return 
    try: 
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title,link) 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH) 
    except: 
        log("download_video_720pMAX error!\n Do you set the PATH correctly?")

def download_video_LQ(link,SAVE_PATH):
    log("download_video_LQ")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    if ( playlistOrNot(link,"single_video") == False):
        return 
    try:
        yt = YouTube(link,on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title)
        stream = yt.streams.first()
        stream.download(SAVE_PATH)
    except:
        log("download_video_LQ: error!")

def downloadVideoWithRezolution(SAVE_PATH,link,rezolution):
    try:
        yt = YouTube(link,on_progress_callback=on_progress) 
        print_info_downloading_single_file(yt.title,link)
        yt.streams.filter(res=rezolution, progressive=False).first().download(SAVE_PATH)
    except: 
        log("Download video in "+str(rezolution)+"p failed")


# # Download Functions : Playlists : Videos
# -----------------------------------------

def download_video_playlist_720pMAX(link,SAVE_PATH):
    log("download_video_playlist_720pMAX()")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    if ( playlistOrNot(link,"playlist") == False ):
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
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
                count_ += 1
            except:
                log("download_video_playlist_720pMAX: fail during downloading, does video has age restictions?")
    except:
        log("download_video_playlist_720pMAX: error!")  

def download_video_playlist_LQ(link,SAVE_PATH):
    log("download_video_playlist_LQ()")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    if ( playlistOrNot(link,"playlist") == False ):
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
                log("download_video_playlist_720pMAX: fail during downloading")
    except:
        log("download_video_playlist_720pMAX: error!")  

# # Download Functions : Playlists : Audios
#------------------------------------------

def download_mp3_audio_playlist_with_thumbnails(link : str,SAVE_PATH : str):
    log("download_mp3_audio_playlist_with_thumbnails()")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    problem_occured_during_downloading = False
    file_exists_flag = False
    try:
        if ( playlistOrNot(link,"playlist") == False ):
            return
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        try:
            for video in playlist.videos:
                temp_link = video.watch_url
                yt = YouTube(temp_link,on_progress_callback=on_progress)    
                file_path = ""
                title = "title"
                # interestingly, assigning a video title to a <string> variable can cause problems (eirher yt.title and video.title)
                try:
                    title = str(yt.title)    # no errors found if it is like that
                except :
                    try:
                        title = str(video.title)
                    except:
                        title = "<can`t_get_title>"
                try:
                    #vid_title = video.title  
                    #print_info_downloading_playlist(str(count_),total,vid_title,temp_link)
                    inf =  (time_now()+" downloading ("+str(count_)+"/"+str(total)+") "+title+" "+temp_link)
                    log(inf)
                except: 
                    log("Error: download_mp3_audio_playlist_with_thumbnails(): print info error ")
                try:
                    debuglog("to fileExsists commes:"+" "+SAVE_PATH+" "+title+" "+temp_link)
                    file_exists_flag = False
                    file_exists_flag = fileExsists(SAVE_PATH,title,temp_link)
                except: 
                    log(bcolors.WARNING+"Error: "+bcolors.ENDC+"download_mp3_audio_playlist_with_thumbnails: file Exists flag error")
                    log("I'm downloading just in case")
                    file_exists_flag = False # its better to download it if it didnt existeed
                if file_exists_flag == True:
                    count_+=1
                else:    #download: 
                    try:
                        audio = download_audio(yt,"mp3", SAVE_PATH)
                        file_path = os.path.join(SAVE_PATH,audio.default_filename) # 
                        file_path = convert_to_mp3_with_metadata(file_path)
                        set_meta_data(yt, SAVE_PATH, file_path , temp_link, "playlist" , playlist.title )
                        count_ += 1
                        try:
                            files_links.append(temp_link) # can be helpful if there are duplicates in playlist
                            files_names.append(video.title+".mp3")
                        except:
                            log("Erorr: download_mp3_audio_playlist_with_thumbnails: cant append downloaded data do list ") 
                    except:
                        log("Error: download_mp3_audio_playlist_with_thumbnails: some problem occured during dowloading!")
                        problem_occured_during_downloading = True
        except:
            log("Erorr: download_mp3_audio_playlist_with_thumbnails(): main loop error")
           # print("wysylam temp_link do fileExists" + temp_link) 
            
                # fixed: finding duplicate not always works beacause during converting some chars can by cutted of like : // , / , |
           
    except:
        log("erorr during downloading playlist <-- download_mp3_audio_playlist_with_thumbnails() : ")
        
    if (problem_occured_during_downloading):
        log("sleep before next download")
        time.sleep(20) # sleep 10 s
        if(check_internet_connection()):
            thread_download() # download again
    
    #print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")     


def download_mp3_audio_playlist(link,SAVE_PATH):
    log("download_mp3_audio_playlist")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    try:
        if ( playlistOrNot(link,"playlist") == False ):
            return
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_),total,video.title,temp_link)
                audio = download_audio(yt,"mp3", SAVE_PATH)
                file_path = os.path.join(SAVE_PATH, audio.default_filename)
                file_path = convert_to_mp3_with_metadata(file_path)
                count_ += 1
            except:
                log("download_mp3_audio_playlist_f(): some problem occured during dowloading!")
    except:
        log("Erorr during downloading palylist")
        log("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")  


def download_mp4_audio_playlist(link,SAVE_PATH):
    log("download_mp4_audio_playlist")
    log("Downloading started "+time_now()+"\n---------------------------------------")
    try:
        if ( playlistOrNot(link,"playlist") == False ):
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
                log("some problem occured during dowloading!")
    except:
        log("Erorr during downloading palylist")
        log("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")

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
        log("Merge failed")

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
                except: log("couldnt remove mp4 temporary file")
            except: log("couldnt write and close audiofile")
        except: log("couldnt make AdioFileClip")
    except:
        log("convert_to_mp3_with_metadata function error!")


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
        if mode == "playlist":
            tag.album = playlist_title
        try:
            tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'thumbnail.jpg'),'rb').read(), 'image/jpeg')
        except:
            log("couldnt make an image by using tag")
        tag.save(version=eyed3.id3.ID3_V2_3) # important if u want to see effect also in windwos media player
        remove_file(SAVE_PATH,"thumbnail.jpg")             
    except:
        log("Couldn`t make an image to file "+file_path)


# # inside functions 
# -------------------

def check_internet_connection(host='http://google.com'):
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
                log("cant set tag to array"+filename)  
    except:
        log("fileExsists() error during getting gilenames")              
    debuglog("fileExsists() : Setting infromation to lists ended.")

def fileExsists( SAVE_PATH : str, yt_title : str, link_to_video : str):
    debuglog("---fileExsists(): start() ")
    name_exists = False
    link_exists = False
    try:
        # compare URL`s` from .mp3 files metadata from SAVE_PATH to video link that can be downloaded  
        for i in range (len(files_links)):
            if files_links[i] == link_to_video:
                debuglog("file exists:(by a link) for "+link_to_video)
                link_exists = True
                break
        
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
                log("error: fileExsists(): cant rename a file")
                return True # dont download, becaouse it would overwrite file with the other file
        else:
            log("------File NOT Exists------(Not supported case)")
            return True     # case as above 
        
    except: log("cant find anything in arrays or even print them")
    log("------File NOT Exists rare case------")
    return False

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

# dont show log info during downloading in cmd, but store it in log file
def hiddenlog(infos : str):
    try:
        logs.append(remove_non_ascii(infos)+"\n")
    except: print(bcolors.WARNING+"ERORR: hiddenlog(): adding to logs list error"+bcolors.ENDC)

# for additional log infos 
def debuglog(infos : str):
    append = append_debug_details_to_logs
    show = show_cmd_details
    if(append and show):
        log(infos)
    elif(append and not show):
        hiddenlog(infos)
    elif(not append and show):
        print(infos)

# (debug) print additional information in cmd
# for masive infos  
def detail(*infos):
    if show_cmd_details == True:
        for info in infos:
            print(info)
    
def make_log(logs:list):
    if make_logs == False:
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
        print("make_log(): some problem occured!")

def exit_handler(): # TODO it should had been here for saving log file but havent worked yet
    print("test before exit")
    
# usage: remember last save location (SAVE_PATH)
# update or create file with new content (old content erased)
def updateFile(filename : str, content : str):
    try:
        file = open(filename,"w")
        file.write(content)
        file.close()
    except:
        log(bcolors.WARNING+"Erorr: updateFile()"+bcolors.ENDC)

# usage: remember last save location (SAVE_PATH)    
def read_file(filename : str):
    try:
        file = open(filename, 'r')
        content = file.read()
        file.close()
        return content
    except FileNotFoundError:
        updateFile(filename,"set path here")
        return "set path here"

def print_info_downloading_single_file(video_title : str, video_link : str):
        info = time_now()+" downloading "+video_title+" "+video_link
        log(info)
        
def print_info_downloading_playlist(count_: str, total: str , video_title : str , video_link : str):
    info = "time_info"
    try:
        info = time_now()+" downloading ("+str(count_)+"/"+str(total)+") "+video_title+" "+video_link
    except: print("error: print_info_downloading_playlist(): making info error")
    try:
        log(info)
    except: print ("error: print_info_downloading_playlist(): making log error") 

def playlistOrNot(linkk,confirm):
    print("checking playlist or single video:")
    print(link)
    if link.__contains__('https://www.youtube.com/playlist?list=') and confirm == "playlist":
        print("playlist confirmed")
        print("--------------------------------")
        return True
    if not (linkk.__contains__('https://www.youtube.com/playlist?list=')) and confirm == "single_video":
        print("single video confirmed")
        print("--------------------------------")
        return True
    else:
        msg.showinfo(title="err", message="UserErorr: link adressing playlist, not one film or vice versa")
        print("UserErorr: link adressing playlist, not one film or vice versa")
        return False # https://www.youtube.com/watch?v=uXKdU_Nm-Kk


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
        debuglog(bcolors.WARNING+"Error in This_Two_Are_The_Same() "+bcolors.ENDC) # massive if True
    
    return False

# # Button Fucntions (Tkinter)
# ----------------------------

def enableDownloadButton():
    if ButtonDownload["state"] == "disabled":
        ButtonDownload["state"] = "normal" #other options: active

def buttonActionConfirmThePath():
    global SAVE_PATH
    SAVE_PATH = textBoxPath.get(1.0, "end-1c")
    updateFile("last_location.txt",SAVE_PATH)
    SAVE_PATH = change_backslashes(SAVE_PATH)
    labelPath.config(text = "Provided Input: "+SAVE_PATH)
    enableDownloadButton()

def checkBoxAction_makeLogs( var ):
    global make_logs
    if int(var) == 1:
        make_logs = True
        print("checkBoxAction_makeLogs() ->  make_logs = true")
    elif int(var) == 0:
        make_logs = False
        print("checkBoxAction_makeLogs() -> make_logs = false")

def checkBoxAction_makeDetailedLogs( var ):
    global append_debug_details_to_logs  
    if int(var) == 1:
        append_debug_details_to_logs = True
        print("checkBoxAction_makeDetailedLogs() ->  append_debug_details_to_logs = true")
    elif int(var) == 0:
        append_debug_details_to_logs = False
        print("checkBoxAction_makeDetailedLogs() -> append_debug_details_to_logs = false")

def checkBoxAction_cmdDetails (var):
    global show_cmd_details  
    if int(var) == 1:
        show_cmd_details = True
        print("checkBoxAction_cmdDetails() ->  show_cmd_details = true")
    elif int(var) == 0:
        show_cmd_details = False
        print("checkBoxAction_cmdDetails() -> show_cmd_details = false")

# prevent tkinter winodw from being freezed during downloading 
# or run multiple downloads at once (mess in logs)
def thread_download():
    files_links.clear()
    files_names.clear()
    fulfill_lists()
    label_download.configure(text="Downloading in progress")
    new_thread = threading.Thread(target=startDownloading).start()
    
def startDownloading():
    global link 
    global SAVE_PATH
    
    link = textBoxDownloadLink.get(1.0, "end-1c")
    #label_download.config(text = "Provided Input: "+link)  
    chosen_plan = Combobox.get()
    #print("Try download a video\nlink: ",link,"\nSAVE_PATH:",SAVE_PATH)
    #print("--------------------------------")
    
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
    
   # if chosen_plan == "videos : whole channel 720p MAX":
   #     download_chanel_720pMAX(link,SAVE_PATH)
    
    
    label_download.configure(text=" ") 
    log("Downloading endend "+time_now()+"\n---------------------------------------")
    #downloading_thread.join()
    make_log(logs)
    msg.showinfo(title="information", message="Download ended")     
    
def browse(): # TODO , not working yet 
   global SAVE_PATH
   try: 
       browse_path = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
       SAVE_PATH = browse_path
       SAVE_PATH = change_backslashes(SAVE_PATH) # for windows usage 
       textBoxPath.delete("1.0","end")
       textBoxPath.insert("end-1c",browse_path)
   except:
       log("ygui: browse(): anything hasn`t been setted")
        
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
#downloading_thread = threading.Thread(target=startDownloading)

def main():
            
    global textBoxPath
    global ButtonDownload
    global labelPath
    global textBoxDownloadLink
    global Combobox
    global label_download
    global threads

    print(time_now())
    log("start "+time_now()+"\n")
    
    # Top level window -------------------------

    frame = tkinter.Tk()
    frame.title(frame_title)
    frame.geometry(frame_geometry)
    frame.configure(background=main_collor)
    myFont = font.Font(family=gui_font, size=gui_font_size)

    # Browse Button -----------------------------

    browseBtn = tkinter.Button(frame,text = "Browse", command = browse)
    browseBtn['font'] = myFont
    browseBtn.pack()
    
    # textbox for the path ----------------------

    textBoxPath = tkinter.Text(frame,height = 5,width = 20) # TextBox Creation
    if len(auto_fill_SAVE_PATH)>0:
        auto_fill = auto_fill_SAVE_PATH
        auto_fill = change_backslashes(auto_fill)
        textBoxPath.insert("end-1c",auto_fill)
    else:
        last_location = read_file("last_location.txt")
        textBoxPath.insert("end-1c",last_location)
    textBoxPath.configure(background="#FFFFFF")
    textBoxPath.pack()

    # Label with info <enetering the path> ------

    labelPath = tkinter.Label(frame, text = "Enter here^ a PATH where to download:^",background=main_collor,fg=TEXT_collor)
    labelPath['font'] = myFont
    labelPath.pack()

    # Button to confirm tha path ----------------

    ButtonPathConfirm = tkinter.Button(frame,text = "confirm the PATH", command = buttonActionConfirmThePath)
    ButtonPathConfirm['font'] = myFont
    ButtonPathConfirm.pack()

    # Textbox for the link ----------------------

    textBoxDownloadLink = tkinter.Text(frame,height = 5,width = 20)  
    if len(auto_fill_link_field)>0:
        textBoxDownloadLink.insert("end-1c",auto_fill_link_field)
    textBoxDownloadLink.pack()
 
    # Label with info for the <confirm the path>

    label_enterLink = tkinter.Label(frame,text="Enter here a YouTube Link ^", background=main_collor,fg=TEXT_collor)
    label_enterLink['font'] = myFont
    label_enterLink.pack()

    # Button to confirm download ----------------

    ButtonDownload = tkinter.Button(frame,text = "confirm link and download", command = thread_download ) #buttonActionDownload
    ButtonDownload.pack()
    ButtonDownload["state"] = "disabled"  # button is disabled at start 
    ButtonDownload['font'] = myFont
    
    # Combobox to choose an option of download---

    downloadType = DownloadType
    Combobox=ttk.Combobox(frame,values=downloadType.downloadTypes,width=30,state = "readonly",font=myFont)
    Combobox.current(2) # show first option 
    frame.option_add('*TCombobox*Listbox.font', myFont) # apply font to combobox list
    Combobox.pack()

    # Label with downloading info ---------------

    label_download = tkinter.Label(frame,text=" ", background=main_collor,fg="#1aff1a")
    label_download['font'] = myFont
    label_download.pack()    

    # checkBoxes to make logs -------------------------
     
    var1 = tkinter.IntVar() # if not this, the 2 checkboxes would be touched in 1 click (graphically)
    var2 = tkinter.IntVar()
    var3 = tkinter.IntVar()
    c1 = tkinter.Checkbutton(frame, 
                             text='make logs',
                             variable=var1,
                             onvalue=1,
                             offvalue=0 ,
                             background=main_collor,
                             fg=TEXT_collor,
                             selectcolor="blue",
                             command=lambda:checkBoxAction_makeLogs(str(var1.get())) )
    c1['font'] = myFont
    c1.pack()
    c2 = tkinter.Checkbutton(frame, 
                             text='add debug details to logs',
                             variable=var2, 
                             onvalue=1,
                             offvalue=0, 
                             background=main_collor,
                             fg=TEXT_collor,
                             selectcolor="blue",
                             command=lambda:checkBoxAction_makeDetailedLogs(str(var2.get())))
    c2['font'] = myFont
    c2.pack()
    c3 = tkinter.Checkbutton(frame, 
                         text='show debug details in cmd',
                         variable=var3, 
                         onvalue=1,
                         offvalue=0, 
                         background=main_collor,
                         fg=TEXT_collor,
                         selectcolor="blue",
                         command=lambda:checkBoxAction_cmdDetails(str(var3.get())))
    c3['font'] = myFont
    #c3.select()
    c3.pack()

    frame.resizable(width=False, height=False)

    frame.mainloop()
    
    #if downloading_thread.is_alive():
    #    downloading_thread.join() # wait until thread is executed
    
    return 0
    
main()



#downloading_process.join()

#atexit.register(exit_handler)
