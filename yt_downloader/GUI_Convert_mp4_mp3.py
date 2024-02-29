import tkinter
import tkinter.font as font
from Converters import convert_to_mp3_with_metadata

# pod miniaturki ------------
import eyed3
from eyed3.id3.frames import ImageFrame
from pytube import YouTube
import requests
#-------------------------

from pytube import YouTube

from GUI_Variables import GUI_VARS
from Logs import errorLog
# textBoxPath.delete("1.0", "end")
class GUI_ConvertMP4toMP3:
    window = ...
    img_label = ...
    textBoxImgPath = ...
    textBoxSongPath = ...
    songPATH = ""
    imagePATH = ""
    labelPathSong = ...
    labelPathImage = ...
    LoadImgToFileBtn = ...

# askfile - ask user for a file
# asktypes: ask_imagePATH /
def askfile():
    from tkinter import Tk  # from tkinter import Tk for Python 3.x
    from tkinter.filedialog import askopenfilename
    Tk().withdraw()  # dont show tkinter gui
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    sourcePATH = rf'{filename}'
    filetype = filename[-4:]
    print(f'[GUI_Convert_mp4_mp3.py -> askfile()]: filename : {filename} / filetype: {filetype} / source path: {sourcePATH}')
    GUI_ConvertMP4toMP3.textBoxSongPath.insert("end-1c", sourcePATH)
    return filename

def convert():
    songtitleMP4 = GUI_ConvertMP4toMP3.textBoxSongPath.get(1.0, "end-1c")
    status = convert_to_mp3_with_metadata(songtitleMP4,deleteFile=False)
    if status is False:
        status = convert_to_mp3_with_metadata(songtitleMP4 + ".mp4",deleteFile=False)
    if status is False:
        print("[GUI_Convert_mp4_mp3.py -> convert() ] Can not convert song")


def loadBackgoroundImage():
    frame = GUI_ConvertMP4toMP3.window
    try:
        img = tkinter.PhotoImage(file="background.png")
        img_label = tkinter.Label(frame, image=img)
        frame.attributes('-alpha', 0.8)  # frame transparency
        # frame.wm_attributes('-transparentcolor',main_collor)       # even whole frame can be transparent
        img_label.place(x=0, y=0)
    except:
        errorLog("main(): couldnt`t load background image")
        main_collor_ = GUI_VARS.dark_cyan
        frame.configure(background=GUI_VARS.main_collor_)

def startGUI():
    frame = tkinter.Tk()
    GUI_ConvertMP4toMP3.window = frame
    loadBackgoroundImage()

    frame.geometry(GUI_VARS.frame_geometry)
    frame.resizable(width=False, height=False)

    myFont = font.Font(family=GUI_VARS.gui_font, size=GUI_VARS.gui_font_size)

    # text boxes
    #textBoxImgPath = tkinter.Text(frame, height=2, width=39, font=('Helvetica 12 bold'),
     #                          foreground="black").place(x=60, y=120)
    textBoxSongPath = tkinter.Text(frame, height=2, width=39, font=('Helvetica 12 bold'))
    textBoxSongPath.place(x=60, y=210)

    # labels
    labelPath = tkinter.Label(frame, text="Mp4 to Mp3 converter", background=GUI_VARS.main_collor_,
                              fg=GUI_VARS.TEXT_collor, font=myFont).place(x=220, y=50)

    #labelPathImage = tkinter.Label(frame, text="Enter here^ a PATH where to put a converted file^",
    #                               background=GUI_VARS.main_collor_,
    #                              fg=GUI_VARS.TEXT_collor, font=myFont).place(x=60, y=170)

    labelPathSong = tkinter.Label(frame, text="Enter here a PATH to mp4 file^", background=GUI_VARS.main_collor_,
                                    fg=GUI_VARS.TEXT_collor)
    labelPathSong['font'] = myFont
    labelPathSong.place(x=110, y=258)


    #Buttons

    ConvertButton = tkinter.Button(frame, text="download image", command=convert).place(x=120,
                                                                                        y=290)  # buttonActionDownload

    #askSongPath = tkinter.Button(frame, text="Browse song", command=lambda: askfile(), font=myFont).place(x=410,
     #                                                                                                        y=120)

    askSongPath = tkinter.Button(frame, text="Browse_song", command=lambda: askfile(),
                                     font=myFont).place(x=410,
                                                        y=180)


    GUI_ConvertMP4toMP3.textBoxSongPath = textBoxSongPath
    #GUI_ConvertMP4toMP3.textBoxImgPath = textBoxImgPath
    GUI_ConvertMP4toMP3.LoadImgToFileBtn = ConvertButton

    frame.mainloop()

    return 0
