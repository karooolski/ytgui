from datetime import datetime
import os
from tkinter import messagebox as msg
import eyed3
from eyed3.id3.frames import ImageFrame
# from eyed3.id3 import tag
import eyed3.id3 as id3

from Logs import debuglog
from StringManipulation import *

from logs import *
import urllib.request  # check internet connection

class Files_info:
    files_links = []
    files_names = []

from Logs import *

# # DEBUG :
# ---------------



# # Editing Files Functions
# -------------------------

def remove_file(location, filename):
    path = os.path.join(location, filename)
    os.remove(path)

# # inside functions
# -------------------
def is_internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False

# True - file exists
# False - file not exists, can be downloaded
def fileExsists(SAVE_PATH: str, yt_title: str, link_to_video: str,files_links,files_names):
    debuglog("[fileExsists] ---fileExsists(): start() ")
    name_exists = False
    link_exists = False
    if(len(Files_info.files_names) == 0 and len(Files_info.files_links)==0):
        log("[.Utils]: [fileExsists]: function see files names and files links as zeros")
        return False
    try:
        debuglog("[fileExsists] comparing files links with existing link")
        # compare URL`s` from .mp3 files metadata from SAVE_PATH to video link that can be downloaded
        for i in range(len(Files_info.files_links)):
            if Files_info.files_links[i] == link_to_video:
                debuglog("[fileExsists] file exists:(by a link) for " + link_to_video)
                link_exists = True
                break

        debuglog("[fileExsists] comparing filenames")
        # checking if in SAVE_PATH exists file with the same filename as yt_title
        file_name = " "
        for i in range(len(Files_info.files_names)):
            if This_Two_Are_The_Same(Files_info.files_names[i], yt_title) or Files_info.files_names[
                i] == yt_title:  # files_names[i] == link_to_video:
                file_name = Files_info.files_names[i]
                debuglog("[fileExsists] file exists:(by tilte) for \"" + yt_title + "\"")
                name_exists = True
                break
        # Verdict:
        if name_exists and link_exists:
            info = "[fileExsists] ------File Exists------(by name and link)"
            print(bcolors.WARNING + info + bcolors.ENDC)
            debuglog(info)
            return True
        elif not name_exists and link_exists:  # f.ex. renamed arlier .mp3 files witch had the same name as others
            debuglog("[fileExsists] ------File Exists------(by link only)")
            return True
        elif not name_exists and not link_exists:
            debuglog("[fileExsists]------File NOT Exists------(at all)")
            return False
        # next attempt:
        # there can can be a video with the same title but other content -> changing tittle to <title><date>:
        elif name_exists and not link_exists and not file_name.__contains__(".mp4"):
            log("[fileExsists] maybe there is audio with the same title but with an other content ...")
            try:
                type = " "
                debuglog("[fileExsists] filename: " + str(file_name))
                if file_name.__contains__(".mp4"):
                    type = ".mp4"
                elif file_name.__contains__(".mp3"):
                    type = ".mp3"
                newname = str(str(file_name[:-3]) + " " + time_now_clean() + str(type))
                log("[fileExsists] newname: " + newname)
                #log(bcolors.WARNING +"[fileExsists] fileExsists(): name_exists and link not exists: renaming file"+ bcolors.ENDC)
                warning("[.Utils]: [fileExsists]: name_exists and link not exists: renaming file")
                os.rename(SAVE_PATH + "/" + file_name, SAVE_PATH + "/" + newname)  # so rename it
                log("[fileExsists] ------File NOT Exists but the same name existed earlier------")
                return False  # and download file with the same name as one changed above
            except:
                errorLog("[fileExsists] cant rename a file")
                return True  # dont download, becaouse it would overwrite file with the other file
        else:
            debuglog("[fileExsists] ------File NOT / Exists ------(Not supported case)")
            return True  # case as above

    except:
        errorLog("[fileExsists] cant find anything in arrays or even print them")
    errorLog("[fileExsists] ------File NOT Exists rare case------")
    return False


# this program also need '/' slashes in the path like in linux instead "\"
def change_backslashes(word):
    if len(word) == 0:
        return ("")
    ex = '\\'
    l = list(word)
    for i in range(len(word)):
        # w = print(word[i])
        if l[i] == ex:
            l[i] = '/'
        s = ''.join(l)
    return (s)


def change_backslashes_to_windows_type(word):
    ex = '/'
    l = list(word)
    for i in range(len(word)):
        # w = print(word[i])
        if l[i] == ex:
            l[i] = '\\'
        s = ''.join(l)
    return (s)


def stringReplace(word, toReplace, replacement):
    word_ = list(word)
    for i in range(len(word)):
        if word_[i] == toReplace:
            word_[i] = replacement
        output = ''.join(word_)
    return (output)


def time_now():
    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
    date_time = stringReplace(date_time, '/', '.')
    return date_time


def time_now_clean():
    now = datetime.now()
    date_time = now.strftime("%Y %m %d, %H %M %S")
    return date_time


def exit_handler():  # TODO it should had been here for saving log file but havent worked yet
    print("test before exit")


def print_info_downloading_single_file(video_title: str, video_link: str):
    try:
        info = time_now() + " downloading " + video_title + " " + video_link
        log(info)
    except:
        errorLog("print_info_downloading_single_file(): couldn`t make log")


def print_info_downloading_playlist(count_: str, total: str, video_title: str, video_link: str):
    infos = "time_info"

    try:
        infos = time_now() + " downloading (" + str(count_) + "/" + str(total) + ") " + video_title + " " + video_link
        # label_download.configure(text="downloading "+ str(count_) +" from " + str(total))
    except:
        errorLog("[print_info_downloading_playlist]: making info error")
        title = remove_non_ascii(video_title)
        if title == "":
            title == "<ASCI_REMOVED>"
        infos = time_now() + " downloading (" + str(count_) + "/" + str(total) + ") " + video_title + " " + video_link
    try:
        info(infos)
    except:
        errorLog("[print_info_downloading_playlist]: making log error")


def validLink(link_, confirm):
    print("[validLink] provided link: " + link_)
    try:
        debuglog("[Utils.validLink] checking playlist or single video and others: ")
        if link_ == "" or link_ == " ":
            errorLog("[Utils.validLink]You have provided empty link")
            msg.showinfo(title="Error",
                         message="UserErorr: You have provided empty link")
            return False
        if link_.__contains__('https://www.youtube.com/watch?v=') and link_.__contains__(
                '&list=') and confirm == "single_video":
            debuglog("single_video confirmed inside playlist")
            return True
        if link_.__contains__('https://www.youtube.com/playlist?list=') and confirm == "playlist":
            print("playlist confirmed")
            print("--------------------------------")
            return True
        if not (link_.__contains__('https://www.youtube.com/playlist?list=')) and link_.__contains__(
                "https://www.youtube.com/watch?v=") and confirm == "single_video":
            print("[validLink] single video confirmed")
            print("--------------------------------")
            return True
        if link_.__contains__('https://www.youtube.com/shorts/') and confirm == "single_video":
            debuglog("[validLink] downloading short")
            return True
        else:
            msg.showinfo(title="Error",
                         message="UserErorr: Propably you have entered some wrong input, check link and the path")
            errorLog("UserErorr: Propably you have entered some wrong input, check link and the path")
            return False  # https://www.youtube.com/watch?v=uXKdU_Nm-Kk
    except:
        errorLog("Error: validLink(): some problem occured")





# sometimes you want to download a video during watching playlist
# the link contains watch and list in the same but for
# def singleVideoFromPlaylist():

def remove_unnecesary_chars(text: str):
    text = stringReplace(text, ".", "")
    text = stringReplace(text, ",", "")
    text = stringReplace(text, "|", "")
    text = stringReplace(text, "/", "")
    text = stringReplace(text, "`", "")
    text = stringReplace(text, "'", "")
    text = stringReplace(text, "\"", "")
    text = stringReplace(text, ":", "")
    text = stringReplace(text, "#", "")
    text = stringReplace(text, "?", "")
    text = stringReplace(text, " ", "")
    # text = stringReplace(text,"💙","") remove_non_ascii(): doing it
    # text = stringReplace(text,"🇳🇴","")
    return text




def fill_lists(link,title):
    try:
        Files_info.files_links.append(link)  # can be helpful if there are duplicates in playlist
        Files_info.files_names.append(title + ".mp3")
    except:
        errorLog("couldnt fill lists (append new information)")

def fulfill_lists(SAVE_PATH):
    try:
        if int(Files_info.files_names.__len__()) < 1:
            debuglog("[fulfill_lists]: appending infromation to lists")
            try:
                for filename in os.listdir(SAVE_PATH):

                    if filename.__contains__(".mp4") or filename.__contains__(".mp3"):
                        debuglog("appending \"" + filename + "\"")
                        Files_info.files_names.append(filename)

                    if filename.__contains__(".mp3"):
                        path = os.path.join(SAVE_PATH, filename)
                        path = change_backslashes(path)
                        # audiofile = eyed3.load(path)
                        tag = id3.Tag()
                        tag.parse(path)
                        # if not tag.artist_url == None:
                        debuglog("appending " + str(tag.artist_url) + " for \"" + filename + "\"")
                        Files_info.files_links.append(str(tag.artist_url))
            except:
                errorLog("[Utils: fulfill_lists] cant set tag to array" + filename)
    except:
        errorLog("fileExsists() error during getting filenames")
    debuglog("fileExsists() : Setting infromation to lists ended.")

# celaring lists: files_links and files_names
def clearLists():
    Files_info.files_links.clear()
    Files_info.files_names.clear()

# compare two filenames
# taking into account that during download some chacacters can be removed
def This_Two_Are_The_Same(dir_i_: str, yt_title_):
    try:
        # debuglog("This_Two_Are_The_Same()?\""+dir_i_+"\" \""+yt_title_+"\"") # massive

        # i want to edit those strings locally so i need to copy it
        dir_i = dir_i_
        yt_title = yt_title_

        # dir_i_ has ".mp3" because it is taken from filesystem and yt_title_ doesnt have that:
        dir_i = dir_i_[:-4]

        # most common case : the names are exacly the same :
        if dir_i == yt_title:
            debuglog("dir_i == yt_title: \"" + dir_i + "\" \"" + yt_title + "\"")
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
            debuglog("dir_i == yt_title: after removed unnecesary chars \"" + dir_i + "\" \"" + yt_title + "\"")
            return True

        # case : title has other asci characters that can`t be cought by remove_unnecesary_chars()

        dir_i = remove_non_ascii(dir_i)
        yt_title = remove_non_ascii(yt_title)

        if dir_i == yt_title and not dir_i == "":
            debuglog("dir_i == yt_title after removed non asci characters: \"" + dir_i + "\" \"" + yt_title + "\"")
            return True

        # case : if the title consist of only non asci character f.ex chinese/japanese titles
        # then after removal there is nothing to compare, empty string

        if (dir_i == yt_title and dir_i == ""):
            debuglog("(dir_i == yt_title and dir_i ==\"\", nothing here: \"" + dir_i + "\" \"" + yt_title + "\"")
            # it means remove_non_ascii() remved the whote title (whole title consisted of non asci characters)
            # and can`t compare it`
            return False

        else:

            return False
    except:
        errorLog("Error: This_Two_Are_The_Same() ")  # massive if True

    return False
