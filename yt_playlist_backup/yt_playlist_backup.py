# start 2022 10 16 14 ..
from datetime import datetime
from pytube import YouTube 
from pytube import Playlist
from contextlib import redirect_stdout

# yt playlist backup: 
# Backup: playlist details to a txt file: 
# reason: yt sometimes can delete your playlist with no reason 
# Note that playlist musn`t be private!

global link 
global list_of_links 

global backup_one_playlist
global backup_more_playlists

# choose if you want to backup 1 or more playlists 
# 0 means OFF : option disabled , 1 means ON : option enabled 
backup_one_playlist = 0
backup_more_playlists = 1

# just enter link to playlist here, and run a script (backup_one_playlist = 1)
link = ""

# or backup more than one list  (backup_more_playlists = 1)
list_of_links = [
        "", # playlist 1 
        ""  # playlist 2
        ]

# running script:           <windows>: python yt_playlist_backup.py
# output :                  "<date> <playlist_title> .txt", 
# output file location:     same as this script location 

def stringReplace(word,toReplace,replacement):
    ex = toReplace
    l = list(word)
    for i in range(len(word)):
        if l[i] == ex:
            l[i] = replacement
        s = ''.join(l)
    return(s)

def time_for_filename():
    now =  datetime.now()
    date_time = now.strftime("%Y %m %d %H %M %S")
    return date_time

def time_now():
    now =  datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time = stringReplace(date_time,'/','.')       
    return date_time

def playlistOrNot(linkk,confirm):
    global link 
    #print("checking playlist or single video:")
    #print(link)
    if link.__contains__('https://www.youtube.com/playlist?list=') and confirm == "playlist":
        print("playlist confirmed")
        return link
    if not (linkk.__contains__('https://www.youtube.com/playlist?list=')) and confirm == "single_video":
        print("single video confirmed")
        return link
    else:
        print("UserErorr: link adressing playlist, not one film")
        return ' ' # https://www.youtube.com/watch?v=uXKdU_Nm-Kk

#def print_info_downloading_playlist(count_: str, total: str , video_title: str, video_link:str):  
 #   try:
 #       f = open("out.txt",'w')
 #       out_string = time_now()+"Video ("+str(count_)+"/"+str(total)+") "+video_title,"+",video_link
 #       f.write("out_string")
#    except:
#        print ("cant write a file")
                #print_info_downloading_playlist(str(count_),str(total),str(video.title),str(temp_video_link))
                #out_string = print(time_now(),"Video (",str(count_),"/",str(total),") ",video.title,"+",temp_video_link)
        
def print_playlist_info_to_file(link):
    link = playlistOrNot(link,"playlist")
    playlist = Playlist(link)
    print("backuping playlist",playlist.title,"...")
    filename = time_for_filename() + " " + playlist.title + ".txt"
    f = open(filename,'w')
    try:
        print("Progress: (showing onlny <count>%10 == 0)\n")
        count_ = 1
        total = str(playlist.length)
        f.write(time_now()+"\n")
        try:
            for video in playlist.videos:
                temp_video_link = video.watch_url
                out_string = "initial_data"
                try:
                    # do not add video.author here, because then it will not work, maybe some video titles cant be written to txt file (windows)
                    out_string ="\n"+"("+str(count_)+"/"+str(total)+") "+str(video.title)+" , "+"\n"+temp_video_link+"\n"+"author:"+video.channel_url+"\n"
                except:
                    print("out_string error")
                #print(out_string)
                if int(count_) % 10 == 0:
                    print(count_,"/",total)
                try:
                    f.write(out_string)
                except: a = 1 #print ("can`t write to file!") # it would be shown too often with no reason, but it`s fine
                count_ += 1
        except:
            print("error of function print write")
    except:
        print("Worst error")
    f.write("\n"+time_now())
    f.close()

def big_backup(): # add as much playlists as you want to be backuped at once and run it instead main
    global link
    global list_of_links 
    for i in list_of_links:
        try:
            link = i
            print_playlist_info_to_file(i)
        except: print("that playlist is propably private: ",i)    

def main():
    try:
        print_playlist_info_to_file(link)
    except:print("is your playlist private?")

if backup_one_playlist == 1:
    main()
    
if backup_more_playlists == 1:
    big_backup()    
    
#main()


#    list = [5,"g",3]
#    for i in list:
#        print (i)
