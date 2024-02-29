import tkinter
import tkinter.font as font

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
class GUI_AlbumImageChanger:
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
def askfile(asktype):
    from tkinter import Tk  # from tkinter import Tk for Python 3.x
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    print(filename)

    sourcePATH = rf'{filename}'

    filetype = filename[-4:]
    print(f'filetype: {filetype}')

    if asktype == "ask_imagePATH":
        GUI_AlbumImageChanger.textBoxImgPath.insert("end-1c", sourcePATH)
    elif asktype == "ask_songPATH":
        GUI_AlbumImageChanger.textBoxSongPath.insert("end-1c", sourcePATH)

    return filename

def AddAlbumImageToSong():
    imgPath = GUI_AlbumImageChanger.textBoxImgPath.get(1.0, "end-1c")
    songPath = GUI_AlbumImageChanger.textBoxSongPath.get(1.0, "end-1c")
    print(f'imgpath{imgPath}\nsongPath:{songPath}')
    try:
        audiofile = eyed3.load(rf'{songPath}')
        if not audiofile.tag:
            audiofile.initTag()
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(rf'{imgPath}', 'rb').read(), 'image/jpeg')
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
        print("Audiofile saved")
    except:
        print("Problem occured wuth setting image")

def try_get_title(yt : YouTube):
    title = "Noname"
    try:
        title = yt.title
    except:
        pass
    return title

def downloadImage():
    import os
    a = 1

    PATH = GUI_AlbumImageChanger.textBoxImgPath.get(1.0, "end-1c")
    LINK = GUI_AlbumImageChanger.textBoxSongPath.get(1.0, "end-1c")
    yt = YouTube(LINK)
    print(f"path:{PATH}, link: {LINK}")
    try:

        yt_image = requests.get(yt.thumbnail_url)  # download video thumbnail
        with open(os.path.join(PATH, "thumbnail.jpg"), 'wb') as f:
            f.write(yt_image.content)
            f.close()
    except:
        pass
    print(f"title:{try_get_title(yt)}")


def startGUI():
    frame = tkinter.Tk()
    GUI_AlbumImageChanger.window = frame
    try:
        img = tkinter.PhotoImage(file="background.png")
        img_label = tkinter.Label(frame, image=img)
        GUI_AlbumImageChanger.img_label = img_label
        frame.attributes('-alpha', 0.8)  # frame transparency
        # frame.wm_attributes('-transparentcolor',main_collor)       # even whole frame can be transparent
        img_label.place(x=0, y=0)
    except:
        errorLog("main(): couldnt`t load background image")
        main_collor_ = GUI_VARS.dark_cyan
        frame.configure(background=GUI_VARS.main_collor_)

    frame.geometry(GUI_VARS.frame_geometry)
    frame.resizable(width=False, height=False)

    myFont = font.Font(family=GUI_VARS.gui_font, size=GUI_VARS.gui_font_size)

    labelPath = tkinter.Label(frame, text="Album Image Changer", background=GUI_VARS.main_collor_, fg=GUI_VARS.TEXT_collor, font=myFont)
    labelPath.place(x=220, y=50)

    textBoxImgPath = tkinter.Text(frame, height=2, width=39, font=('Helvetica 12 bold'),
                               foreground="black")
    textBoxImgPath.place(x=60, y=120)
    GUI_AlbumImageChanger.textBoxImgPath = textBoxImgPath

    textBoxSongPath = tkinter.Text(frame, height=2, width=39, font=('Helvetica 12 bold'))
    textBoxSongPath.place(x=60, y=210)

    GUI_AlbumImageChanger.textBoxSongPath = textBoxSongPath

    LoadImgToFileBtn = tkinter.Button(frame, text="download image", command=downloadImage)  # buttonActionDownload
    LoadImgToFileBtn.place(x=120, y=290)
    GUI_AlbumImageChanger.LoadImgToFileBtn = LoadImgToFileBtn

    labelPathImage = tkinter.Label(frame, text="Enter here^ a PATH where to download^", background=GUI_VARS.main_collor_,
                              fg=GUI_VARS.TEXT_collor, font=myFont)
    labelPathImage.place(x=60, y=170)

    labelPathSong = tkinter.Label(frame, text="Enter here an YouTube Link ^", background=main_collor_,
                                    fg=GUI_VARS.TEXT_collor)
    labelPathSong['font'] = myFont
    labelPathSong.place(x=110, y=258)

    askImagePathBtn = tkinter.Button(frame, text="Browse_img", command=lambda: askfile("ask_imagePATH"), font=myFont).place(x=410,
                                                                                                             y=120)

    askSongPath = tkinter.Button(frame, text="Browse_song", command=lambda: askfile("ask_songPATH"),
                                     font=myFont).place(x=410,
                                                        y=180)


    frame.mainloop()

    return 0
