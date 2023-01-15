# GUI -------------------------------------
import tkinter
from tkinter import ttk
from tkinter import messagebox as msg
#from tkinter import messagebox, filedialog # TODO may be useful in the future
import tkinter.font as font
# PYTUBE API ------------------------------
from pytube import Playlist
from pytube import YouTube 
from pytube.cli import on_progress #this module contains the built in progress bar. (console)
# System -------------------------------------------------
import os
from datetime import datetime
import requests
# System :: If file exists -------------------------------
import os.path
from os.path import exists
# System :: making before exit action (saving log)
# import atexit
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
    log("download_mp3_audio_with_thumbnail()") 
    if ( playlistOrNot(link,"single_video") == False):
        return 
    try:
         yt = YouTube(link,on_progress_callback=on_progress)
    except:
         log("mp3 download connection error")
    try:
        print_info_downloading_single_file(yt.title,link)
        audio = download_audio(yt,"mp3", SAVE_PATH)
        file_path = ""
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except: 
            log("couldnt convert mp4 to mp3")
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
            log("Couldn`t make an image to file "+file_path)
    except:
        log("download_mp3_audio_with_thumbnail: (function) dowloading error!")    

def download_mp4_audio(link,SAVE_PATH):
    log("download_mp4_audio()")
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
    if ( playlistOrNot(link,"single_video") == False):
        return 
    try:
         yt = YouTube(link,on_progress_callback=on_progress)
         print_info_downloading_single_file(yt.title,link)
    except:
         log("mp3 download connection error")
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
    try:  
        yt = YouTube(link,on_progress_callback=on_progress)
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

def download_mp3_audio_playlist_with_thumbnails(link,SAVE_PATH):
    log("download_mp3_audio_playlist_with_thumbnails()")
    try:
        if ( playlistOrNot(link,"playlist") == False ):
            return
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link,on_progress_callback=on_progress)
            file_path = ""
            print_info_downloading_playlist(str(count_),total,video.title,temp_link)
            
            # second way to find a file: 
            path_to_file = str ( str ( SAVE_PATH )  + "/" + str ( yt.title ) + ".mp3" ) 
            file_exists = exists(path_to_file)
            # if file_exists :
            
            flag = 0 # flag idicates if the name of the yt.title and a file in the SAVE_PATH are the same
            
            dir = os.listdir(SAVE_PATH)
            # way to print dir: 
            for i in range(len(dir)): # iterate thorough filenames in SAVE_PATH location to see if there are some copies 
                if This_Two_Are_The_Same(dir[i],yt.title):
                    #print("-------THESE FILES ARE THE SAME--------")
                    flag = 1
                #print (dir[i],)
            if file_exists or flag == 1: #the same as : if  dir.__contains__(str(yt.title)+".mp3"): 
                log("----File is already exists!---")
                count_ += 1
                # finding duplicate not always works beacause during converting some chars can by cutted of like : // , / , |
            else:    
                # print("file not exists: ")
                #os.system("pause")
                try:
                    audio = download_audio(yt,"mp3", SAVE_PATH)
                    file_path = os.path.join(SAVE_PATH,audio.default_filename) # 
                    file_path = convert_to_mp3_with_metadata(file_path)
                    count_ += 1
                except:
                    log("some problem occured during dowloading!")
                try:
                    yt_image = requests.get(yt.thumbnail_url) # download video thumbnail  
                    with open(os.path.join(SAVE_PATH,"thumbnail.jpg"),'wb') as f: 
                        f.write(yt_image.content)
                    audiofile = eyed3.load(file_path) # convert audio meta data
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
                        log("couldnt make an image by using tag")
                    tag.save(version=eyed3.id3.ID3_V2_3) # important if u want to see effect also in windwos media player
                    remove_file(SAVE_PATH,"thumbnail.jpg")             
                except:
                    log("Couldn`t make an image to file "+file_path)
    except:
        log("Erorr during downloading palylist")
        print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")          

def download_mp3_audio_playlist(link,SAVE_PATH):
    log("download_mp3_audio_playlist")
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

def log_file_name():
    now =  datetime.now()
    date_time = now.strftime("%Y %m %d, %H %M %S")   
    return date_time

def log(infos : str):
    print(infos) # for user during downloading
    logs.append(remove_non_ascii(infos)+"\n")

def make_log(logs:list):
    try:
        logfilename= log_file_name()
        file = open("logs/"+logfilename+".txt","w")
        for i in range (len(logs)):
            file.write(str(logs[i]))
        file.close()
    except FileNotFoundError:
        os.makedirs("logs")
        make_log(logs)
    except: 
        print("make_log(): some problem occured!")

def exit_handler(): # it should have been for saving log file but didnt worked 
    print("test before xit")
    
# usage: remember last save location (SAVE_PATH)
# update or create file with new content (old content erased)
def updateFile(filename : str, content : str):
    file = open(filename,"w")
    file.write(content)
    file.close()

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
    info = time_now()+" downloading ("+str(count_)+"/"+str(total)+") "+video_title+" "+video_link
    log(info)

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

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

def This_Two_Are_The_Same(dir_i : str , yt_title):
    # example : 
    # output : "CHAINSAW MAN - OP1 - Kick Back (Blinding Sunrise Cover Extended Ver).mp3"
    # yt.title:"CHAINSAW MAN - OP1 - Kick Back (Blinding Sunrise Cover Extended Ver.).mp3"
    # 
    # And we dont want to donwnload again olny becaouse the name is different 
    # So i am cutting off every character that after download is vanishing and caomparing names 
    
    path_dir_i = dir_i # this is oputput filename of converting file to a .mp3
    path_dir_i = stringReplace(path_dir_i,".","")
    path_dir_i = stringReplace(path_dir_i,",","")
    path_dir_i = stringReplace(path_dir_i,"|","")
    path_dir_i = stringReplace(path_dir_i,"/","")
    path_dir_i = stringReplace(path_dir_i,"`","")
    path_dir_i = stringReplace(path_dir_i,"'","")
    path_dir_i = stringReplace(path_dir_i,"\"","")
    path_dir_i = stringReplace(path_dir_i,":","")
    path_dir_i = stringReplace(path_dir_i,"#","")
    path_dir_i = stringReplace(path_dir_i," ","")
    #path_dir_i = stringReplace(path_dir_i,"💙","")
    #path_dir_i = stringReplace(path_dir_i,"🇳🇴","")
    
    path_dir_i = remove_non_ascii(path_dir_i) # this should be better than this both at the top
    path_dir_i = path_dir_i[:-3] # removing 'mp3' (last characters at those strings)
    #print("path_dir_i: "+path_dir_i)
    
    path_yt_title =  yt_title # this what yt.title returns
    path_yt_title = stringReplace(path_yt_title,".","")
    path_yt_title = stringReplace(path_yt_title,",","")
    path_yt_title = stringReplace(path_yt_title,"|","")
    path_yt_title = stringReplace(path_yt_title,"/","")
    path_yt_title = stringReplace(path_yt_title,"`","")
    path_yt_title = stringReplace(path_yt_title,"'","")
    path_yt_title = stringReplace(path_yt_title,"\"","")
    path_yt_title = stringReplace(path_yt_title,":","")
    path_yt_title = stringReplace(path_yt_title,"#","")
    path_yt_title = stringReplace(path_yt_title," ","")
    #path_yt_title = stringReplace(path_dir_i,"💙","")
    #path_yt_title = stringReplace(path_dir_i,"🇳🇴","")
    path_yt_title = remove_non_ascii(path_yt_title)
    #print("pathh_yt_title: "+path_yt_title)
    
    if path_dir_i == path_yt_title:
#        print("This 2 are the same")
#        print(path_after_key)
#        print(path_first_key)
        return True
    else:
#        print("This 2 are NOT the same")
#        print(path_dir_i)
#        print(path_yt_title)
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
        
    log("Downloading endend "+time_now()+"\n---------------------------------------")
    make_log(logs)
    
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
logs = []



def main():
            #f.write(info)
    global textBoxPath
    global ButtonDownload
    global labelPath
    global textBoxDownloadLink
    global Combobox

    print(time_now())
    log("start "+time_now()+"\n")
    # Top level window -------------------------

    frame = tkinter.Tk()
    frame.title("YouTube Audio / Video Downloader")
    frame.geometry('500x350')
    frame.configure(background=main_collor)
    myFont = font.Font(family=gui_font, size=gui_font_size)

    # textbox for the path ----------------------

    textBoxPath = tkinter.Text(frame,height = 5,width = 20) # TextBox Creation
    last_location = read_file("last_location.txt")
    textBoxPath.configure(background="#FFFFFF")
    textBoxPath.insert("end-1c",last_location)
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
#atexit.register(exit_handler)
