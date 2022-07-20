import tkinter
from tkinter import ttk
from turtle import color
import tkinter.font as font
from pytube import YouTube 
from pytube.cli import on_progress #this module contains the built in progress bar. 
import time
#https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/

global download_audio 
global download_video
download_audio = 0 
download_video = 1 
# def step():
#     for i in range(5):
#         ws.update_idletasks()
#         pb1['value'] += 20
#         time.sleep(1)

#def temp_text(e):
#   textBoxPath.delete(0,"end")

ASCI_grey = "#808080"
TEXT_collor = "white"

def changeDownladType():
    global download_audio 
    global download_video
    if download_audio == 1:
        download_audio = 0
        download_video = 1
        ButtonAudioVideoDownloadChange.configure(text="Now you will download video ", command = changeDownladType)
        print("downlading video mode ON")
    else:
        if download_audio == 0:
            download_audio = 1
            download_video = 0
            ButtonAudioVideoDownloadChange.configure(text="Now you will download audio ", command = changeDownladType)
            print("downloading audio mode ON")

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
    try: 
        yt = YouTube(link,on_progress_callback=on_progress) 
    except: 
        print("YouTube(link) error: Connection Failed") #to handle exception 
    #   pb.start()
    #   step()
    global download_video
    if download_video == 1:
        try: 
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)    
        #if download_audio == 1:
        #    yt.streams.get_audio_only("mp4").download(SAVE_PATH)
        except: 
            print("yt.streams.filter error!\n Do you set the PATH correctly?") 
    if download_audio == 1:
        try:
            yt.streams.get_audio_only("mp4").download(SAVE_PATH)
        except:
            print("yt.streams.get_audio_only: error!")
    #pb.stop()
    print('Finished working!') 
  
# TextBox Creation
textBoxPath = tkinter.Text(frame,height = 5,width = 20)
#textbox = Entry(win, bg="white", width=50, borderwidth=2)
#textBoxPath.insert(0,"Ener here a PATH")
textBoxPath.pack()
# Button Creation
printButtonPath = tkinter.Button(frame,text = "confirm the PATH", command = buttonActionConfirmThePath)
printButtonPath['font'] = myFont
printButtonPath.pack()
# Label Creation
labelPath = tkinter.Label(frame, text = "Enter here^ a PATH where to download:^",background=ASCI_grey,fg=TEXT_collor)
labelPath['font'] = myFont
labelPath.pack()
#textBoxPath.bind("<FocusIn>", temp_text)


textBoxDownload = tkinter.Text(frame,height = 5,width = 20)  
textBoxDownload.pack()
printButtonDownload = tkinter.Button(frame,text = "confirm link and download", command = buttonActionDownload)
printButtonDownload.pack()
printButtonDownload["state"] = "disabled"  # button is disabled at start 
printButtonDownload['font'] = myFont
label_download = tkinter.Label(frame,text="Enter here a YouTube Link ^", background=ASCI_grey,fg=TEXT_collor)
label_download['font'] = myFont
label_download.pack()
#frame.grid()

# audio / video change button 

temp_string = ""
if download_video == 1:
    temp_string = "video"
else:
    if download_audio == 1:
        temp_string = "audio"   



ButtonAudioVideoDownloadChange = tkinter.Button(frame,text="Now you will download "+temp_string, command = changeDownladType)
ButtonAudioVideoDownloadChange['font'] = myFont
ButtonAudioVideoDownloadChange.pack()
label_audioVideoChange = tkinter.Label(frame,text="You can change wether you want do download video / audio ^", background=ASCI_grey,fg=TEXT_collor)
label_audioVideoChange['font'] = myFont
label_audioVideoChange.pack()

# progressbar
# pb = ttk.Progressbar(
#     frame,
#     orient='horizontal',
#     mode='indeterminate',
#     length=280
# )
# place the progressbar
#pb.pack()

frame.mainloop()



#SAVE_PATH = "" # where to save #/home/karol/Pulpit/yt
