import tkinter
from pytube import YouTube 
#https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/

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
frame.title("TextBox Input")
frame.geometry('500x300')

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
        yt = YouTube(link) 
    except: 
        print("YouTube(link) error: Connection Failed") #to handle exception 
    try: 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
    except: 
        print("yt.streams.filter error!\n Do you set the PATH correctly?") 
    print('Finished working!') 
  
# TextBox Creation
textBoxPath = tkinter.Text(frame,height = 5,width = 20)
textBoxPath.pack()
# Button Creation
printButton = tkinter.Button(frame,text = "confirm the PATH", command = buttonActionConfirmThePath)
printButton.pack()
# Label Creation
labelPath = tkinter.Label(frame, text = "")
labelPath.pack()

textBoxDownload = tkinter.Text(frame,height = 5,width = 20)  
textBoxDownload.pack()
printButton2 = tkinter.Button(frame,text = "confirm link and download", command = buttonActionDownload)
printButton2.pack()
label_download = tkinter.Label(frame,text="")
label_download.pack()



frame.mainloop()



#SAVE_PATH = "" # where to save #/home/karol/Pulpit/yt
