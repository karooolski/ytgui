from pytube import Playlist
from pytube import YouTube
import sys
import youtube_dl  # pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"
# from pytube.cli import on_progress #this module contains the built in progress bar. (console)
# from pytube import Channel
# System -------------------------------------------------
# import os
from youtube_dl.utils import sanitize_filename
import threading
# from tkinter import messagebox as msg
# import eyed3
from eyed3.id3.frames import ImageFrame
# from eyed3.id3 import tag
# import eyed3.id3 as id3

import yt_dlp


import requests

import Debug_Options
# from Logs import *
# from Logs import debuglog
# from Utils import *
from Converters import *
from UserInfo import *
from GUI_Variables import *
from StringManipulation import *

import yt_dlp

class DownloadInfo:
    logs = []
    files_links = []
    files_names = []


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
        # "videos : whole channel 720p MAX"
    ]


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


# @staticmethod
def on_progress(
        stream: Stream, chunk: bytes, bytes_remaining: int
) -> None:  # pylint: disable=W0613
    filesize = stream.filesize
    # print("stream.filesize = "+str(filesize))
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)



# # Download Functions : Audios
# -----------------------------

def ytdl_download_mp3_audio_with_thumbnail(link: str, SAVE_PATH: str):
    func_title = "[ytdl_download_mp3_audio_with_thumbnail]: "
    try:
        log(f"{func_title} Function started " + time_now() + "\n---------------------------------------")
        if validLink(link, "single_video") == False:
            return False
        download_result = alternative_download_mp3_2(link, SAVE_PATH, "single_video", count_=0, total=1, playlist_title="MUZA 3")
        return download_result # True / False
    except:
        errorLog(f"{func_title}Function error")
        return False


def download_mp3_audio_with_thumbnail(link: str, SAVE_PATH: str):
    func_name = "[download_mp3_audio_with_thumbnail]: "

    log(func_name + "download_mp3_audio_with_thumbnail()\nDownloading started " + time_now() + "\n---------------------------------------")

    if (validLink(link, "single_video") == False):
        return

    yt = YouTube(link, on_progress_callback=on_progress)

    try:
        print_info_downloading_single_file(yt.title, link)

        if fileExsists(SAVE_PATH, yt.title, link, DownloadInfo.files_links, DownloadInfo.files_names):
            log(func_name + "----File is already exists!---")
            msg.showinfo(title="information", message="File is already exists in current path")
            return

        audio = download_audio(yt, SAVE_PATH)
        file_path = ""
        try:
            file_path = os.path.join(SAVE_PATH, audio.default_filename)
            file_path = convert_to_mp3_with_metadata(file_path)
        except:
            errorLog("Error: download_mp3_audio_with_thumbnail():couldn`t convert mp4 to mp3")
        set_meta_data(yt, SAVE_PATH, file_path, link, "single_video", "None")

        try:
            DownloadInfo.files_links.append(link)  # can be helpful if there are duplicates in playlist
            DownloadInfo.files_names.append(yt.title + ".mp3")
        except:
            errorLog("Erorr: download_mp3_audio_with_thumbnail(): cant append downloaded data do list ")
    except:
        errorLog("download_mp3_audio_with_thumbnail: whole function send error message!")
        try:
            debuglog("Retry download audio: ")
            alternative_download_mp3(link, SAVE_PATH, "single_video")
        except:
            errorLog("[download_mp3_audio_with_thumbnail] second method of download also didnt work")


def download_mp4_audio(link, SAVE_PATH):
    log("download_mp4_audio()\nDownloading started " + time_now() + "\n---------------------------------------")
    if (validLink(link, "single_video") == False):
        return
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title, link)
        yt.streams.get_audio_only("mp4").download(SAVE_PATH)
    except:
        errorLog("yt.streams.get_audio_only: error!")


# Usage: download video in 1080p and merge with audio
def downloadAudioToBeMerged(link, SAVE_PATH):  # download audio onldy
    global title  # variable for merge and rename purposes
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title, link)
        # yt.streams.filter(abr="160kbps", progressive=False).first().download(SAVE_PATH,filename="audiocbd")
        yt.streams.get_audio_only("mp4").download(SAVE_PATH, filename="audiomerge.mp4")
        title = yt.title
        return True
    except:
        errorLog("Error: downloadAudioToBeMerged(): Download audio failed")
        return False


def download_mp3_audio(link, SAVE_PATH):
    log("download_mp3_audio()\nDownloading started " + time_now() + "\n---------------------------------------")
    if (validLink(link, "single_video") == False):
        return
    yt = YouTube(link, on_progress_callback=on_progress)
    if yt == False:
        return
    print_info_downloading_single_file(yt.title, link)
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
def downloadVideo_1080p_toBeMerged(link, SAVE_PATH):  # download video only
    log("downloadVideo_1080p_toBeMerged\nDownloading started " + time_now() + "\n---------------------------------------")
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        if yt == False:
            return False
        try:
            print_info_downloading_single_file(yt.title, link)
        except:
            pass
        yt.streams.filter(res="1080p", progressive=False).first().download(SAVE_PATH, filename="videomerge.mp4")
        return True
    except:
        errorLog("Error: downloadVideo_1080p_toBeMerged(): Download video failed")
        return False

    # usage: downloading mp3 , # inner function for other functions


def download_audio(_yt_: YouTube, save_path: str):
    debuglog("[download_audio]: save path = " + save_path)
    debuglog("yt: " + str(_yt_))
    try:
        _audio_ = _yt_.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        _audio_.download(save_path)
        print("output audio : " + str(_audio_))
        errorLog("download_audio: problem occured during downloading! ")
        debuglog("[download_audio]: end downloading")
        return _audio_  # returning audiofile (mp4) to be converted to mp3
    except:
        errorLog("[download_audio]: download video (function) error!")


def tryPrintPlaylistInfo(link):
    func_title = '[Dondload.py -> tryPrintPlaylistInfo()]: '
    print(f"{func_title}:Playlist video urls: ")
    try:
        playlist = Playlist(link)
        playlist_title = playlist.title
        count_ = 1
        total = str(playlist.length)

        urls = playlist.video_urls
        for url in urls:
            print(f"{func_title} {count_}/{total}: {url}")
            count_ += 1

        # for video in playlist.videos:
        #     tmp_link = video.watch_url
        #     #yt = YouTube(tmp_link, on_progress_callback=on_progress)
        #     title = ""
        #     try:
        #         title = video.title
        #     except:
        #         title = "<can`t read title>"
        #     print(f"{func_title}: {count_}/{total}: link:{tmp_link}, title:{title} playlist_title:{playlist_title}")
        #     count_ += 1
        return True
    except:
        errorLog(func_title + "can`t print playlist info")
        return False


def try_get_title(yt : YouTube):
    title = "None"
    try:
        title = yt.title
    except:
        pass
    return title




# --------------------------------
# Download MP3  
# --------------------------------



# mode: single_video, playlist
def alternative_download_mp3(link, SAVE_PATH, mode, count_=0, total=1, playlist_title="None", one_more_time=False):
    yt = YouTube(link)
    func_title = "[alternative_download_mp3]: "
    try:
        debuglog(func_title + "Start working")
        destination = ""
        ydl_opts = {
            'outtmpl': SAVE_PATH + '/%(title)s.mp4',  # %(ext)s
            'format': 'best',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }
        debuglog(func_title + "try download : " + link)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            link_to_char = '' + link
            name, _format_ = "", ""
            debuglog(func_title + "Extracting information from web page")
            result = ydl.extract_info(link_to_char, download=False)
            debuglog(func_title + "Extractinging process completed")
            _title_ = try_get_title(yt)
            if _title_ == "None":
                _title_ = result['title']  # debuglog(func_title + "Title setted")
            title = sanitize_filename(_title_)  # for example if filename contains || it is turned into __
            file_exists = fileExsists(SAVE_PATH, title, link, DownloadInfo.files_links, DownloadInfo.files_names)
            debuglog(func_title + "file exists check setted")
            print_info_downloading_playlist(str(count_), str(total), title, link)
            if file_exists:
                log(func_title + "File already exists")
                return False
            _format_ = result['ext']  # debuglog(func_title + "Format setted")
            author = result['uploader']  # debuglog(func_title + "uploader setted")
            audio_file = SAVE_PATH + title + '.' + _format_  # debuglog(func_title + "audiofile setted")
            ydl.download([link_to_char])
            if _title_ != title:
                try:
                    os.rename(_title_,title)
                    log("File renamed! #201920dsmzx")
                except:
                    errorLog("[Download][alternative_download_mp3]: can not rename file ! ")

            filepath = SAVE_PATH + '/' + title + '.' + _format_
            ydl.encode('')
            convering_result = convert_to_mp3_with_metadatax2(SAVE_PATH, _title_)
            if convering_result:
                filepath = SAVE_PATH + '/' + title + '.mp3'
                yt = YouTube(link)
                set_meta_data(yt, SAVE_PATH, filepath, link, mode, playlist_title, title, author)
                fill_lists(link, title)
                return True
            return False
    except:  # downlaod ended not successfully, try one more time
        return_code = False
        if not one_more_time:  # if it is one more time try to download and it is also failed, then do not go there (download) again
            errorLog(func_title + " Function error with downloading " + link)
            warning("[.Download]: [alternative_download_mp3]: another try to download a file")
            one_more_time_download = alternative_download_mp3_2(link, SAVE_PATH, mode, count_, total, playlist_title,
                                                              one_more_time=True)
            if one_more_time_download == True:
                return_code = True
            else:
                errorLog("[.Download]: [alternative_download_mp3]: another try to download a file failed")
        return return_code

# 2023 09 23 01 28
def alternative_download_mp3_2(link, SAVE_PATH, mode, count_=0, total=1, playlist_title="None", one_more_time=False, download_only_mp4=False):
    func_title = "[alternative_download_mp3_2]: "
    try:
        debuglog(func_title + "Start working")
        destination = ""
        ydl_opts = {
            'outtmpl': SAVE_PATH + '/%(title)s.mp4',  # %(ext)s
            'format': 'best',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }
        debuglog(func_title + "try download : " + link)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydtd = yt_dlp.YoutubeDL()
            result = ydtd.extract_info(link, download=False)
            _title_ = result['title']
            title = sanitize_filename(_title_) # for example if filename contains || it is turned into __
            _format_ = result['ext']

            link_to_char = '' + link
            name, _format_ = "", ""
            file_exists = fileExsists(SAVE_PATH, title, link, DownloadInfo.files_links, DownloadInfo.files_names)
            debuglog(func_title + "file exists check setted")
            print_info_downloading_playlist(str(count_), str(total), title, link)
            if file_exists:
                log(func_title + "File already exists")
                return False
            _format_ = result['ext']  # debuglog(func_title + "Format setted")
            author = result['uploader']  # debuglog(func_title + "uploader setted")
            audio_file = SAVE_PATH + title + '.' + _format_  # debuglog(func_title + "audiofile setted")
            ydl.download([link_to_char])
            # if _title_ != title:
            #     try:
            #         os.rename(_title_,title)
            #         log("File renamed! #201920dsmzx")
            #     except:
            #         errorLog("[Download][alternative_download_mp3]: can not rename file ! ")
            filepath = SAVE_PATH + '/' + title + '.' + _format_
            ydl.encode('')

            if download_only_mp4 == True:
                return True
        
            convering_result = convert_to_mp3_with_metadatax2(SAVE_PATH, title)

            if convering_result is False:
                info("Filename of song setted by windows is differend than filename received from youtube, now im searching thorugh files to find mp4 file with song and tranform it into mp3 and set thumbnail")
                filename, result_bool = find_mp4_file(SAVE_PATH)
                if result_bool:
                    filepath = SAVE_PATH + '/' + filename
                    convering_result = convert_to_mp3_with_metadatax2(SAVE_PATH, filename, NotAddMp4=True)
                    title = filename[:-4] # without mp4

            if convering_result:
                filepath = SAVE_PATH + '/' + title + '.mp3'
                yt = YouTube(link)
                set_meta_data(yt, SAVE_PATH, filepath, link, mode, playlist_title, title, author)
                fill_lists(link, title)
                return True
            return False
    except:  # downlaod ended not successfully, try one more time
        return_code = False
        if not one_more_time:  # if it is one more time try to download and it is also failed, then do not go there (download) again
            errorLog(func_title + " Function error with downloading " + link)
            warning("[Download.py]: -> alternative_download_mp3(): another try to download a file")
            one_more_time_download = alternative_download_mp3(link, SAVE_PATH, mode, count_, total, playlist_title,
                                                              one_more_time=True)
            if one_more_time_download == True:
                return_code = True
            else:
                errorLog("[Download.py] -> alternative_download_mp3(): another try to download a file failed")
                debuglog("[.Download]: [alternative_download_mp3]: Try download album image for future use")
                yt_get_thumbnail(link,SAVE_PATH)
        return return_code

def alternative_download_audio_mp3_playlist(link,
                                            SAVE_PATH):  # https://www.youtube.com/playlist?list=PLi3mp5yIcf2o2-JgUijKAdE9yMEh83iHY
    func_name = '[alternative_download_audio_mp3_playlist]: '
    debuglog(func_name + "try doing opts")
    try:
        playlist = Playlist(link)
        playlist_title = playlist.title
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:

            if Debug.break_downloading:  # Stop downloading if user click "stop downloading" button
                return True

            tmp_link = video.watch_url
            # yt = YouTube(tmp_link, on_progress_callback=on_progress)
            alternative_download_mp3_2(tmp_link, SAVE_PATH, "playlist", count_, int(total), playlist_title)
            count_ += 1
        return True
    except:
        errorLog(func_name + "can`t download playlist also in alternative way")
        return False

# new 2025-04-23 based by yt-dlp
def download_video2(link, SAVE_PATH):
    youtube_dl_options = {
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
        'format': 'best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        return ydl.download([link])


# inner function
def alternative_download_video(link, SAVE_PATH):
    func_title = "[alternative_download_video]: "
    debuglog(func_title + "Start working")
    ydl_opts = {
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
        'format': 'best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            link_as_char = '' + link
            name, _format_ = "", ""
            result = ydl.extract_info(link_as_char, download=False)
            title = result['title']
            _format_ = result['ext']
            audio_file = SAVE_PATH + title + '.' + _format_
            # name = ydl_opts['%(titles)s'];
            debuglog(func_title + "Extracted info: title : " + title + " , format: " + _format_)
            debuglog(func_title + "audiofile = " + audio_file)
            ydl.download([link_as_char])
            return True
    except:
        errorLog(func_title + "Can not donwload video in alternative way too")
        return False


def download_video_720pMAX(link, SAVE_PATH):
    func_title = "[download_video_720pMAX]: "
    log("download_video_720pMAX()\nDownloading started " + time_now() + "\n---------------------------------------")
    if (validLink(link, "single_video") == False):
        return
    try:

        yt = YouTube(link, on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title, link)
        debuglog("printed info")
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
    except:
        try:
            errorLog("download_video_720pMAX(): Some error occured during download, now the second attempt is executed")
            alternative_download_video(link, SAVE_PATH)
            # ydl_opts = {
            #     'outtmpl': SAVE_PATH+'/%(title)s.%(ext)s'
            #     }
            # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #     link_to_char = ''+link
            #     name, _format_ = "", ""
            #     result = ydl.extract_info(link_to_char,download=False)
            #     title = result['title']
            #     _format_ = result['ext']
            #     audio_file = SAVE_PATH+title+'.'+_format_
            #     #name = ydl_opts['%(titles)s'];
            #     debuglog(func_title + "Extracted info: title : "+title+" , format: "+_format_)
            #     debuglog(func_title + "audiofile = "+audio_file)
            #     #ydl.download([link_to_char])
        except:
            errorLog(func_title + "\n Did you set the PATH correctly? , PATH: " + SAVE_PATH)


def download_video_LQ(link, SAVE_PATH):
    log("download_video_LQ\nDownloading started " + time_now() + "\n---------------------------------------")
    if (validLink(link, "single_video") == False):
        return
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title, link)
        stream = yt.streams.first()
        stream.download(SAVE_PATH)
    except:
        errorLog("download_video_LQ: error!")


def downloadVideoWithRezolution(SAVE_PATH, link, rezolution):
    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        print_info_downloading_single_file(yt.title, link)
        yt.streams.filter(res=rezolution, progressive=False).first().download(SAVE_PATH)
    except:
        errorLog("Download video in " + str(rezolution) + "p failed")


# # Download Functions : Playlists : Videos
# -----------------------------------------

def download_video_playlist_720pMAX(link, SAVE_PATH):
    log("download_video_playlist_720pMAX()\nDownloading started " + time_now() + "\n---------------------------------------")
    if (validLink(link, "playlist") == False):
        return
    # total = 0
    # try:
    #    playlist = Playlist(link)
    #    for video in playlist.videos:
    #        total += 1
    # except:
    #    errorLog("download_video_playlist_720pMAX: ")
    try:
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link, on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_), total, video.title, temp_link)
                # print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
                count_ += 1
            except:
                errorLog("download_video_playlist_720pMAX: fail during downloading, does video has age restictions?")
    except:
        errorLog("download_video_playlist_720pMAX: error!")


def download_video_playlist_LQ(link, SAVE_PATH):
    log("download_video_playlist_LQ()\nDownloading started " + time_now() + "\n---------------------------------------")
    if (validLink(link, "playlist") == False):
        return
    try:
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link, on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_), total, video.title, temp_link)
                # print("downloading ("+str(count_)+"/"+str(total)+") "+video.title)
                stream = yt.streams.first()
                stream.download(SAVE_PATH)
                count_ += 1
            except:
                errorLog("download_video_playlist_720pMAX: fail during downloading")
    except:
        errorLog("download_video_playlist_720pMAX: error!")

    # # Download Functions : Playlists : Audios


# ------------------------------------------

def download_mp3_audio_playlist_with_thumbnails(link: str, SAVE_PATH: str, usePytube=False):
    if not usePytube:
        alternative_download_audio_mp3_playlist(link, SAVE_PATH)
        return
    func_title = "[download_mp3_audio_playlist_with_thumbnails]: "
    # global link ; global SAVE_PATH
    # link = link ; SAVE_PATH = SAVE_PATH
    log("download_mp3_audio_playlist_with_thumbnails()")
    log("Downloading started " + time_now() + "\n---------------------------------------")
    problem_occured_during_downloading = False
    file_exists_flag = False

    if (validLink(link, "playlist") == False):
        errorLog("download_mp3_audio_playlist_with_thumbnails : unvalid link")
        return

    debuglog(func_title + "\n SAVE_PATH = " + SAVE_PATH + "\n link = " + link)
    debuglog(func_title + "collecting number of videos to download ...")

    # get exact value of videos in playlist, because playlist.length also counts unvailable videos
    total = 0
    try:
        playlist = Playlist(link)
        total = str(len(playlist.videos))
        total_ppl = str(playlist.length)
        debuglog("counted total: " + str(total) + ", playlist length with unvailable videos: " + str(total_ppl))
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
                yt = YouTube(temp_link, on_progress_callback=on_progress)
                file_path = ""
                title = "title"
                # interestingly, assigning a video title to a <string> variable can cause problems (either yt.title and video.title)
                try:
                    title = str(yt.title)  # no errors found if it is like that
                except:
                    try:
                        title = str(video.title)
                    except:
                        title = "<can`t_get_title>"
                try:
                    # vid_title = video.title
                    # print_info_downloading_playlist(str(count_),total,vid_title,temp_link)
                    inf = str(
                        time_now() + " downloading (" + str(count_) + "/" + str(total) + ") " + title + " " + temp_link)
                    log(inf)
                except:
                    log("Error: download_mp3_audio_playlist_with_thumbnails(): print info error ")
                try:
                    debuglog("to fileExsists commes:" + " " + SAVE_PATH + " " + title + " " + temp_link)
                    file_exists_flag = False
                    file_exists_flag = fileExsists(SAVE_PATH, title, temp_link, DownloadInfo.files_links,
                                                   DownloadInfo.files_names)
                    debuglog("---fileExsists(): end() ")
                except:
                    log(bcolors.WARNING + "Error: " + bcolors.ENDC + "download_mp3_audio_playlist_with_thumbnails: file Exists flag error")
                    log("I'm downloading just in case")
                    file_exists_flag = False  # its better to download it if it didnt existeed
                if file_exists_flag == True:
                    count_ += 1
                else:  # download:
                    try:
                        debuglog("--- start downloading")
                        debuglog("yt: " + str(yt))
                        audio = download_audio(yt, SAVE_PATH)
                        file_path = os.path.join(SAVE_PATH, audio.default_filename)  #
                        file_path = convert_to_mp3_with_metadata(file_path)
                        set_meta_data(yt, SAVE_PATH, file_path, temp_link, "playlist", playlist.title)
                        count_ += 1
                        try:
                            Files_info.files_links.append(
                                temp_link)  # can be helpful if there are duplicates in playlist
                            Files_info.files_names.append(video.title + ".mp3")
                        except:
                            errorLog(
                                func_title + "cant append downloaded data do list ")
                    except:
                        errorLog(
                            func_title + "some problem occured during dowloading!")
                        # problem_occured_during_downloading = True
                        try:
                            info("Startnig another method to download a file")
                            alternative_download_mp3(temp_link, SAVE_PATH)
                            count_ += 1
                        except:
                            errorLog(func_title + "second way to download an mp3 file also didnt work")
        except:
            errorLog("Erorr: download_mp3_audio_playlist_with_thumbnails(): main loop error")
        # print("wysylam temp_link do fileExists" + temp_link)

        # fixed: finding duplicate not always works beacause during converting some chars can by cutted of like : // , / , |

    except:
        errorLog("download_mp3_audio_playlist_with_thumbnails(): erorr during downloading playlist")

    if problem_occured_during_downloading:
        log("sleep before next download")
        time.sleep(20)  # sleep 10 s
        if is_internet_connection():
            thread_download()  # download again

    # print("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")


def download_mp3_audio_playlist(link, SAVE_PATH):
    log("download_mp3_audio_playlist()\nDownloading started " + time_now() + "\n---------------------------------------")
    try:
        if (validLink(link, "playlist") == False):
            return
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link, on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_), total, video.title, temp_link)
                audio = download_audio(yt, SAVE_PATH)
                file_path = os.path.join(SAVE_PATH, audio.default_filename)
                file_path = convert_to_mp3_with_metadata(file_path)
                count_ += 1
            except:
                errorLog("download_mp3_audio_playlist_f(): some problem occured during dowloading!")
    except:
        errorLog("Erorr during downloading palylist")
        errorLog("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")


def download_mp4_audio_playlist(link, SAVE_PATH):
    log("download_mp4_audio_playlist()\nDownloading started " + time_now() + "\n---------------------------------------")
    try:
        if (validLink(link, "playlist") == False):
            return
        playlist = Playlist(link)
        count_ = 1
        total = str(playlist.length)
        for video in playlist.videos:
            temp_link = video.watch_url
            yt = YouTube(temp_link, on_progress_callback=on_progress)
            try:
                print_info_downloading_playlist(str(count_), total, video.title, temp_link)
                try:
                    yt.streams.get_audio_only("mp4").download(SAVE_PATH)
                except:
                    log("download_mp4_audio_playlist: Stream download error")
                count_ += 1
            except:
                errorLog("some problem occured during dowloading!")
    except:
        errorLog("Erorr during downloading palylist")
        errorLog("Check if: \n 1) playlist is NOT private \n 2) your link contains \'list\' ")

def find_mp4_file(SAVE_PATH : str):
    """
    2023 11 03 01 44
    Finds mp4 file, used when mp4 -> mp3 converter recives wrong filename,
    because filename is atomatically setted up during download ,
    and infroamtion that i recive from download function can has different chacacters in filename.
    :param SAVE_PATH:
    :return:
    """
    log("[find_mp4_file] Received wrong tilte in comparison to filename setted by windows, Try to find mp4 file in files.")
    try:
        for filename in os.listdir(SAVE_PATH):
            path = os.path.join(SAVE_PATH,filename)
            if os.path.isfile(path) and path.__contains__(".mp4"):
                debuglog(f"[find_mp4_file] found: {filename} in {SAVE_PATH}")
                return filename, True
        return "No files found", False
    except:
        errorLog(f"[find_mp4_file]: cant interate thorugh files in {SAVE_PATH}")
        return "Error", False
def convert_to_mp3_with_metadatax2(filepath, filename, NotAddMp4 = False):
    func_title = "convert_to_mp3_with_metadata x2"
    if NotAddMp4:
        file_path = filepath + "/" + filename
    else:
        file_path = filepath + "/" + filename + ".mp4"
    file_exists = os.path.isfile(file_path)
    if not file_exists:
        errorLog(f"[{func_title}]: filepath:{file_path} doesnt exist!")
        return False
    debuglog(func_title + "start, got: ")
    try:
        debuglog(file_path)
    except:
        view = remove_non_ascii(file_path)
        debuglog("ASCI REMOVED : " + view)

    try:
        audio_clip = AudioFileClip(file_path);
        debuglog("Created AudioFileClip")
        file_path = file_path.replace("mp4", "mp3");
        debuglog("new filepath")
        audio_clip.write_audiofile(file_path);
        debuglog("AudioFile writed")
        audio_clip.close();
        debuglog("Audioclip closed")
        os.remove(file_path.replace("mp3", "mp4"));
        debuglog("Removed Mp4 file")  # remove mp4 file
        # return file_path
        return True
    except:
        errorLog("[convert_to_mp3_with_metadatax2] Some problem occured during converting mp4 to mp3!")
        info("Trying another method...")
        try:
            new_name = time_now_clean()
            new_file_path = filepath + "/" + new_name + ".mp4"
            os.replace(file_path, new_file_path)
            convert_to_mp3_with_metadatax2(filepath, new_name)
        except:
            errorLog("[convert_to_mp3_with_metadatax2]: another method also didnt work!")
        return False


def yt_get_thumbnail(link, SAVE_PATH):
    func_title = "[yt_get_thumbnail]"
    print(
        f"(\nlink: {link}\nSAVE_PATH: {SAVE_PATH}\n)\n"
    )
    try:
        debuglog(f"{func_title} wczutyje link")
        
        yt = YouTube(link)
        video_id = yt.video_id
        thumbnail_url = f"https://i3.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        
        debuglog(f"{func_title} url: {thumbnail_url}")
        
        # thumbnail_url  = 'https://img.youtube.com/vi/[{vid_id}]/maxresdefault.jpg'
        image = requests.get(thumbnail_url)
        print("got  image")
        print(SAVE_PATH)
        with open(os.path.join(SAVE_PATH, "thumbnail.jpg"), 'wb') as f:
            f.write(image.content)
            f.close()
        return True
    except Exception as ex:
        errorLog(f"[yt_get_thumbnail] error: {str(ex)}")
        return False


# setting metadata for mp3 file: information , albulm image
def set_meta_data(yt: YouTube, SAVE_PATH: str, file_path: str, link: str, mode: str, playlist_title: str,
                  video_title=" ", video_author=" "):
    # mode : "playlist" during dowloading from playlist or other if downloading single file
    debuglog(f"[set_meta_data]: got: \n(\n {SAVE_PATH} + \n + {file_path}  \n + {link}\n)\n")
    try:
        # yt_image = requests.get(yt.thumbnail_url)  # download video thumbnail
        
        # with open(os.path.join(SAVE_PATH, "thumbnail.jpg"), 'wb') as f:
        #     f.write(yt_image.content)
        #     f.close()
        
        downloaded_thumbnail = yt_get_thumbnail(link,SAVE_PATH)
        
        if not downloaded_thumbnail:
            return
        
        audiofile = eyed3.load(file_path)  # convert audio meta data
        
        if not audiofile.tag:
            audiofile.initTag()
        debuglog("[set_meta_data]: creating tag")
        tag = id3.Tag()
        tag.parse(file_path)
        try:
            tag.title = yt.title
        except:
            tag.title = video_title
        try:
            tag.artist = video_author  # yt.author
        except:
            tag.artist = video_author
        tag.artist_url = link
        # tag.audio_source_url  cant be seen in windows10 property, but inside file : yes
        tag._setEncodedBy("ytgui_v" + GUI_VARS.version)
        debuglog("[set_meta_data]: setting tag to a file")
        
        #if mode == "playlist":
        
        tag.album = playlist_title
        
        try:
            tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH, 'thumbnail.jpg'), 'rb').read(),
                           'image/jpeg')
        except:
            errorLog("couldnt make an image by using tag")
        tag.save(version=eyed3.id3.ID3_V2_3)  # important if u want to see effect also in windwos media player
        remove_file(SAVE_PATH, "thumbnail.jpg")
    except:
        errorLog("[set_meta_data]: Couldn`t make an image to file " + file_path)


# prevent tkinter winodw from being freezed during downloading
# or run multiple downloads at once (mess in logs)
def thread_download(GUIobjects, chosen_plan, link, SAVE_PATH):
    if (not is_internet_connection()):
        msg.showinfo(title="information", message="No internet connection detected!")
        return
    try:
        # rodzi blad !!!
        print("AAAAAA")
        Files_info.files_links.clear()
        Files_info.files_names.clear()
        fulfill_lists(SAVE_PATH)
        print("aa")
        # try:
        #    label_download.configure(text="Downloading in progress")
        # except:
        #    pass
        print("********************")
        new_thread = threading.Thread(
            target=lambda: startDownloading(GUIobjects, chosen_plan, link, SAVE_PATH)).start()
        Debug_Options.Debug.break_downloading = False  # if downloading has been stopped then after download i have to change this value egain to false to be ready to another download
    except:
        errorLog(f"Error: thread_download(): some problem occured, chosen plan : {chosen_plan}")


def startDownloading(features, chosen_plan, link, SAVE_PATH):
    #debuglog("startDownloading(): start! ")
    log("Downloading Function starting at: " + time_now() + "\n")

    features.showOnDownloadLabel()

    # global SAVE_PATH
    # global label_download
    # link = UserConfig.link
    # SAVE_PATH = UserConfig.SAVE_PATH
    # link = features.textBoxDownloadLink.get(1.0, "end-1c")
    # label_download.config(text = "Provided Input: "+link)
    # chosen_plan = features.global_Combobox_text #Combobox.get()
    # print("Try download a video\nlink: ",link,"\nSAVE_PATH:",SAVE_PATH)
    # print("--------------------------------")

    # Saving user options

    # userConfig.link = link
    # combobox_index = 0
    # for i in range(len(DownloadType.downloadTypes)):  # getting current combobox id
    #    if DownloadType.downloadTypes[i] == Combobox.get():  # interestingly there is no built-in function in tkinter
    #        break  # to do this for know,
    #    else:
    #        combobox_index += 1
    # userConfig.last_combobox_state = str(combobox_index)  # combobox.current(id)  id -> (String)
    # userConfig.saveConfiguration("userConfig", userConfig)

    # debuglog("cbbx state: " + str(combobox_index))

    # if len(link) < 5:
    #     label_download.configure(text=" ")
    #     debuglog("startDownloading(): wrong link length")
    #     msg.showinfo(title="information", message="Wrong link length")
    #     textBoxDownloadLink.delete("1.0", "end")
    #     textBoxDownloadLink.insert("end-1c", "")
    #     userConfig.link = ""
    #     userConfig.saveConfiguration("userConfig", userConfig)
    #     return

    if chosen_plan == "video 720p MAX":
        download_video_720pMAX(link, SAVE_PATH)

    if chosen_plan == "audio mp3 with thumbnail":
        ytdl_download_mp3_audio_with_thumbnail(link, SAVE_PATH)
        # download_mp3_audio_with_thumbnail(link, SAVE_PATH)

    if chosen_plan == "audio mp3 playlist with thumbnails":
        download_mp3_audio_playlist_with_thumbnails(link, SAVE_PATH)

    if chosen_plan == "audio mp3":
        ytdl_download_mp3_audio_with_thumbnail(link, SAVE_PATH)
        # download_mp3_audio(link, SAVE_PATH)

    if chosen_plan == "audio playlist mp3":
        download_mp3_audio_playlist(link, SAVE_PATH)

    if chosen_plan == "audio mp4":
        download_mp4_audio(link, SAVE_PATH)

    if chosen_plan == "audio playlist mp4":
        download_mp4_audio_playlist(link, SAVE_PATH)

    if chosen_plan == "video playlist 720p MAX":
        download_video_playlist_720pMAX(link, SAVE_PATH)

    if chosen_plan == "video 1080p and merge with audio":
        if (downloadVideo_1080p_toBeMerged(link, SAVE_PATH)):
            if (downloadAudioToBeMerged(link, SAVE_PATH)):
                merge_video_with_audio()

    if chosen_plan == "video in 1080p with no Voice":
        downloadVideoWithRezolution(SAVE_PATH, link, "1080p")  # other: 1440p , 2160p

    if chosen_plan == "video (Lowest quality)":
        download_video_LQ(link, SAVE_PATH)

    if chosen_plan == "video playlist (Lowest quality)":
        download_video_playlist_LQ(link, SAVE_PATH)

        # if chosen_plan == "videos : whole channel 720p MAX":
    #     download_chanel_720pMAX(link,SAVE_PATH)

    # label_download.configure(text=" ")
    log("Downloading endend " + time_now() + "\n---------------------------------------")
    # downloading_thread.join()
    # make_log(Log_list.logs)
    #clearLists()  # clear lists after downlaod everything # cos nie dziala
    #features.buttonBreakDownload["state"] = "disabled"
    features.hideOnDownloadLabel()
    msg.showinfo(title="information", message="Download ended")
    clear_logs()

