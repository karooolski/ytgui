import Debug_Options
import GUI_AlbumImageChanger

FILENAME = "GUI"
# GUI -------------------------------------
import tkinter
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog  # for browse button,
# if you have google drive file stream isntalled on your PC it may output
# <DATE> [17452:ShellIpcClient] shell_ipc_client.cc:129:Connect Can't connect to socket at: \\.\Pipe\GoogleDriveFSPipe_<USER>_shell
# during browsing files, for now I dont know how to surpass it in safe way
# the same output is being produced during using alternative filedialog from PySimpleGUI lib
import tkinter.font as font
import GUI_AlbumImageChanger as gaic
#import GUI_AlbumImageChanger as image_changer
import GUI_DownloadImageCover as image_download
import GUI_Convert_mp4_mp3 as convertermp4
from UserInfo import *
from Utils import *
from Download import *
from logs import *
# # GUI
# ---------------

from GUI_Variables import *

class GUI_Objects:

    global_textboxpath = ""
    global_Combobox_text = ""
    staticLabelDownloading = ...

    def __init__(self):
        self.textBoxPathText = ""
        self.textBoxPath = None
        self.textBoxPathText = ""
        self.textBoxDownloadLink = None
        self.textBoxDownloadLinkText = ""
        self.chosen_plan = ""
        self.buttonBreakDownload = None

    @staticmethod
    def showOnDownloadLabel():
       GUI_Objects.staticLabelDownloading['text'] = "Downlaod in progress"

    @staticmethod
    def hideOnDownloadLabel():
       GUI_Objects.staticLabelDownloading['text'] = ""


    def CreateTextBoxPath(self,frame):
        self.textBoxPath = tkinter.Text(frame, height=2, width=39, font=('Helvetica 12 bold'),
                               foreground="black")  # TextBox Creation
        return self.textBoxPath

    def CreateTextBoxDownloadLink(self,frame):
        self.textBoxDownloadLink = tkinter.Text(frame, height=2, width=39, font=('Helvetica 12 bold'))
        self.textBoxDownloadLink.insert("end-1c", userConfig.link)
        return self.textBoxDownloadLink

    def CreateButtonBreakDownload(self,frame):
        self.buttonBreakDownload = tkinter.Button(frame, text="Stop download", command=lambda:breakDownload(self.buttonBreakDownload), state="disabled")
        return self.buttonBreakDownload

    def get_text_from_textBoxPath(self):
        self.textBoxPathText = self.textBoxPath.get(1.0, "end-1c")
        return self.textBoxPathText

    def get_text_from_textBoxLink(self):
        self.textBoxDownloadLinkText = self.textBoxDownloadLink.get(1.0,"end-1c")
        return self.textBoxDownloadLinkText

    def setLocalComboboxText(self,text):
        self.chosen_plan = text

class GUI_OPTS:
    SAVE_PATH = ""

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
global chosen_plan
chosen_plan = ""
global label_download

# # Button Fucntions (Tkinter)  +  Event Actions
# -----------------------------------------------

def disableDownloadButton():
    downloadButton["state"] = "disabled"


def enableDownloadButton():
    if downloadButton["state"] == "disabled":
        downloadButton["state"] = "normal"  # other options: active


def eventAction_confirmThePath(features):
    try:
        global SAVE_PATH
        SAVE_PATH = features.get_text_from_textBoxPath() #textBoxPath.get(1.0, "end-1c")
        # updateFile("last_location.txt",SAVE_PATH)
        SAVE_PATH = change_backslashes(SAVE_PATH)
        # labelPath.config(text = "Provided Input: "+SAVE_PATH)
        debuglog("eventAction_confirmThePath: len(SAVE_PATH)=" + str(len(SAVE_PATH)) + " SAVE_PATH = " + SAVE_PATH)
        validSavePath(SAVE_PATH)
        userConfig.SAVE_PATH = SAVE_PATH
        userConfig.saveConfiguration("userConfig", userConfig)
    except:
        errorLog("Error: eventAction_confirmThePath()")

def eventAction_SaveLink(features):
    try:
        link = features.textBoxDownloadLink.get(1.0, "end-1c")
        userConfig.link = link
        userConfig.saveConfiguration("userConfig", userConfig)
    except:
        errorLog(f"[{FILENAME}]: [eventAction_SaveLink]: , some error occured")
# combobox will always save its state when you just choose ann option
def event_combobox_saveStateOnClick(event):
    global chosen_plan
    try:
        combobox_option = event.widget.get()
        chosen_plan = combobox_option
        combobox_index = 0
        for i in range(len(DownloadType.downloadTypes)):  # getting current combobox id
            if DownloadType.downloadTypes[
                i] == combobox_option:  # interestingly there is no built-in function in tkinter
                break  # to do this for know,
            else:
                combobox_index += 1
        currentComboboxID = str(combobox_index)  # combobox is setted by sgtring id xd
        debuglog("comboboxGetID(): combobox_inxex=" + currentComboboxID + "  event: " + str(combobox_option))
        userConfig.last_combobox_state = currentComboboxID  # combobox.current(id)  id -> (String)
        userConfig.saveConfiguration("userConfig", userConfig)
    except:
        errorLog("Error: event_combobox_saveStateOnClick(): unexpected problem")

def checkBoxAction_makeLogs(var):
    # global Debug.make_logs
    if int(var) == 1:
        Debug.make_logs = True
        debuglog("checkBoxAction_makeLogs() ->  Debug.make_logs = true")
        userConfig.allow_logs = True
        userConfig.saveConfiguration("userConfig", userConfig)
    elif int(var) == 0:
        Debug.make_logs = False
        debuglog("checkBoxAction_makeLogs() -> Debug.make_logs = false")
        userConfig.allow_logs = False
        userConfig.saveConfiguration("userConfig", userConfig)


def checkBoxAction_makeDetailedLogs(var):
    # global Debug.append_debug_details_to_logs
    global userConfig
    if int(var) == 1:
        Debug.append_debug_details_to_logs = True
        debuglog("checkBoxAction_makeDetailedLogs() ->  Debug.append_debug_details_to_logs = true")
        userConfig.details_in_loggs = True
        userConfig.saveConfiguration("userConfig", userConfig)
    elif int(var) == 0:
        Debug.append_debug_details_to_logs = False
        debuglog("checkBoxAction_makeDetailedLogs() -> Debug.append_debug_details_to_logs = false")
        userConfig.details_in_loggs = False
        userConfig.saveConfiguration("userConfig", userConfig)


def checkBoxAction_cmdDetails(var):
    # global Debug.show_cmd_details
    global userConfig
    if int(var) == 1:
        Debug.show_cmd_details = True
        debuglog("checkBoxAction_cmdDetails() ->  Debug.show_cmd_details = true")
        userConfig.details_in_cmd = True
        userConfig.saveConfiguration("userConfig", userConfig)
    elif int(var) == 0:
        Debug.show_cmd_details = False
        debuglog("checkBoxAction_cmdDetails() -> Debug.show_cmd_details = false")
        userConfig.details_in_cmd = False
        userConfig.saveConfiguration("userConfig", userConfig)


def browse(gui_objects):
    global SAVE_PATH
    global textBoxPath
    try:
        browse_path = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
        SAVE_PATH = browse_path
        SAVE_PATH = change_backslashes(SAVE_PATH)  # for windows usage
        gui_objects.textBoxPath.delete("1.0", "end")
        gui_objects.textBoxPath.insert("end-1c", browse_path)
        userConfig.SAVE_PATH = SAVE_PATH
        userConfig.saveConfiguration("userConfig", userConfig)
        validSavePath(SAVE_PATH)
    except:
        errorLog("Error: browse(): anything hasn`t been setted")

def validSavePath(SAVE_PATH: str):
    isNotEmpty = False
    isNotSpace = False
    isNotHttps = False
    windows_proper = False
    linux_proper = False

    if (not SAVE_PATH == ""): isNotEmpty = True
    if (not SAVE_PATH == " "): isNotSpace = True
    if (not SAVE_PATH.__contains__("https:")): isNotHttps = True
    if (len(SAVE_PATH) >= 3 and SAVE_PATH.__contains__(":/")):  windows_proper = True
    if (len(SAVE_PATH) >= 1 and SAVE_PATH.__contains__("/")): linux_proper = True

    if (isNotEmpty and isNotSpace and isNotHttps and windows_proper or linux_proper):
        debuglog("validSavePath: SAVE_PATH is valid")
        enableDownloadButton()
    else:
        disableDownloadButton()


def downloadAction(gui_objects):
    chosen_plan = combobox.get()
    #userConfig = UserConfig.loadConfiguration("userConfig")
    link = userConfig.link
    SAVE_PATH = userConfig.SAVE_PATH
    gui_objects.buttonBreakDownload["state"] = "normal"
    thread_download(gui_objects,chosen_plan,link,SAVE_PATH)


# Function breaks donwloading
# as an argument is a button: buttonDisableDownload from class GUI_FEATURES
def breakDownload(button):
    button["state"] = "disabled"
    warning(f"[.GUI]: [breakDownload]: Zatrzymano Pobieranie: Status: {Debug_Options.Debug.break_downloading}")
    Debug_Options.Debug.break_downloading = True


def stop_gui(frame):
    Debug_Options.Debug.run_gui = False
    frame.destroy()

def load_background(frame):
    ## Background image
    try:
        img = tkinter.PhotoImage(file="background.png")
        img_label = tkinter.Label(frame, image=img)
        frame.attributes('-alpha', 0.8)  # frame transparency
        # frame.wm_attributes('-transparentcolor',main_collor)       # even whole frame can be transparent
        img_label.place(x=0, y=0)
    except:
        errorLog("main(): couldnt`t load background image")
        main_collor_ = GUI_VARS.dark_cyan
        frame.configure(background=main_collor_)

def openLogsFolder():
    path = rf"./logs"
    path = os.path.realpath(path)
    os.startfile(path)
def start_gui():

    global downloadButton
    global labelPath
    global textBoxDownloadLink
    global combobox
    global userConfig
    global SAVE_PATH
    global threads
    global label_download
    global chosen_plan

    textBoxPath = ""

    x_pos = 100
    y_pos = 20
    main_collor_ = GUI_VARS.main_collor
    # userConfig = UserConfig()
    # userConfig = userConfig.loadConfiguration("userConfig")
    print(time_now())
    log("GUI start at " + time_now() + "\n")

    # Top level window -------------------------

    frame = tkinter.Tk()
    frame.title(GUI_VARS.frame_title + " " + GUI_VARS.version)
    frame.geometry(GUI_VARS.frame_geometry)
    frame.resizable(width=False, height=False)

    gui_objects = GUI_Objects()

    myFont = font.Font(family=GUI_VARS.gui_font, size=GUI_VARS.gui_font_size)

    ## Background image

    img_label = ...
    #load_background(frame)

    try:
        img = tkinter.PhotoImage(file="background.png")
        img_label = tkinter.Label(frame, image=img)
        frame.attributes('-alpha', 0.8)  # frame transparency
        # frame.wm_attributes('-transparentcolor',main_collor)       # even whole frame can be transparent
        img_label.place(x=0, y=0)
    except:
        errorLog("main(): couldnt`t load background image")
        main_collor_ = GUI_VARS.dark_cyan
        frame.configure(background=main_collor_)

    ## background image secod idea

    # frame.wm_attributes("-transparentcolor", 'grey')
    # canv = tkinter.Canvas(frame, width= 1000, height= 1000)
    # canv.create_image(252,253,image=img)  #x,y expands the image size, if range is too big than image is starting moving x:-> / y:down
    # canv.place(x=0,y=0)

    # LABELS

    ## Label title ------

    labelPath = tkinter.Label(frame, text="YTGUI", background=main_collor_, fg=GUI_VARS.TEXT_collor, font=myFont)
    labelPath.place(x=220, y=50)

    ## Label with info <enetering the path> ------

    labelPath = tkinter.Label(frame, text="Enter here^ a PATH where to download:^", background=main_collor_,
                              fg=GUI_VARS.TEXT_collor, font=myFont)
    labelPath.place(x=60, y=170)

    ## Label with info for the <confirm the path>

    label_enterLink = tkinter.Label(frame, text="Enter here^ a YouTube Link ^", background=main_collor_, fg=GUI_VARS.TEXT_collor)
    label_enterLink['font'] = myFont
    label_enterLink.place(x=110, y=258)

    GUI_Objects.staticLabelDownloading = tkinter.Label(frame,text = "downloading in progress", background=main_collor_, fg=GUI_VARS.light_gren)
    GUI_Objects.staticLabelDownloading['font'] = myFont
    GUI_Objects.staticLabelDownloading.place(x=110, y=370)
    GUI_Objects.hideOnDownloadLabel()


    ## canvas labels that are without background

    # canv.create_text(280, 50, text="YTGUI", fill="white", font=('Helvetica 15 bold'))
    # canv.create_text(230, 170, text="Enter here^ a PATH where to download:^", fill="white", font=('Helvetica 13 bold'))
    # canv.create_text(230, 260, text="Enter here^ a YouTube Link ^", fill="white", font=('Helvetica 13 bold'))

    ## Label with downloading info ---------------

    label_download = tkinter.Label(frame, text=" ", background=main_collor_, fg="#1aff1a", font=myFont).place(x=70,
                                                                                                              y=360)

    # TEXTBOXES

    ## textbox for the path ----------------------

    textBoxPath = gui_objects.CreateTextBoxPath(frame)
    last_location = userConfig.SAVE_PATH
    textBoxPath.insert("end-1c", last_location)
    SAVE_PATH = last_location
    debuglog("main(): SAVE_PATH = " + SAVE_PATH)
    textBoxPath.configure(background="white")
    # frame.event_add("<<Mouse_LeftClick_Action>>", "<Button>") # my own event
    # textBoxPath.bind("<<Mouse_LeftClick_Action>>",buttonActionConfirmThePath)
    textBoxPath.bind("<KeyRelease>", lambda x: eventAction_confirmThePath(gui_objects))
    textBoxPath.place(x=60, y=120)

    ## Textbox for the link ----------------------

    textBoxDownloadLink = gui_objects.CreateTextBoxDownloadLink(frame)
    textBoxDownloadLink.bind("<KeyRelease>", lambda x: eventAction_SaveLink(gui_objects))
    textBoxDownloadLink.place(x=60, y=210)

    # Buttons

    ## Browse Button -----------------------------

    convertMP4toMP3Button = tkinter.Button(frame, text="convert MP4 to MP3",
                                           command=convertermp4.startGUI).place(x=50, y=90)  # buttonActionDownload

    browseButton = tkinter.Button(frame, text="Browse", command= lambda: browse(gui_objects), font=myFont).place(x=410, y=120)

    exitButton = tkinter.Button(frame, text="exit", command= lambda: stop_gui(frame), font=myFont).place(x=410,y=70)

    albumImageChangerButton = tkinter.Button(frame, text="Album image changer", command= gaic.startGUI, font=myFont).place(x=10,y=40) # gaic.startGUI()

    albumImageDownloadButton = tkinter.Button(frame, text="Dowload Image", command= image_download.startGUI, font=myFont).place(x=350,y=20)

    openLogsFolderButton = tkinter.Button(frame, text="Logs folder", command= openLogsFolder, font=myFont).place(x=350,y=370)



    ## Button to confirm download ----------------

    downloadButton = tkinter.Button(frame, text="confirm link and download",
                                    command= lambda : downloadAction(gui_objects))  # buttonActionDownload
    downloadButton.place(x=120, y=290)
    downloadButton["state"] = "disabled"  # button is disabled at start
    downloadButton['font'] = myFont

    validSavePath(last_location)  # enable dowload_button if there is already exists a path
    # Combobox to choose an option of download---

    breakDownloadButton = gui_objects.CreateButtonBreakDownload(frame)
    breakDownloadButton['font'] = myFont
    breakDownloadButton.place(x=370,y=290)

    # COMBOBOX

    downloadType = DownloadType

    combobox = ttk.Combobox(frame, values=downloadType.downloadTypes, width=30, state="readonly", font=myFont)

    try:
        currentComboboxID = str(userConfig.last_combobox_state)
        combobox.current(currentComboboxID)  # show last watched option
    except:
        log("main(): incorrect comobox current state,\" " + userConfig.last_combobox_state + " \" problem has been fixed automaticallly")
        combobox.current(0)  # show first option
    frame.option_add('*TCombobox*Listbox.font', myFont)  # apply font to combobox list
    combobox.bind("<<ComboboxSelected>>", event_combobox_saveStateOnClick)  # event listener
    combobox.place(x=70, y=330)

    # CHECKBOXES

    # checkBoxes to make logs -------------------------

    var1 = tkinter.IntVar()  # if not this, the 2 checkboxes would be touched in 1 click (graphically)
    var2 = tkinter.IntVar()
    var3 = tkinter.IntVar()

    makeLogsCheckbox = tkinter.Checkbutton(frame,
                             text='make logs',
                             variable=var1,
                             onvalue=1,
                             offvalue=0,
                             background=main_collor_,
                             fg=GUI_VARS.TEXT_collor,
                             selectcolor="blue",
                             command=lambda: checkBoxAction_makeLogs(str(var1.get())))
    makeLogsCheckbox['font'] = myFont

    if userConfig.allow_logs == True:
        makeLogsCheckbox.select()
        Debug.make_logs = True

    makeLogsCheckbox.place(x=70, y=410)

    debugLogsCheckbox = tkinter.Checkbutton(frame,
                             text='add debug details to logs',
                             variable=var2,
                             onvalue=1,
                             offvalue=0,
                             background=main_collor_,
                             fg=GUI_VARS.TEXT_collor,
                             selectcolor="blue",
                             command=lambda: checkBoxAction_makeDetailedLogs(str(var2.get())))
    debugLogsCheckbox['font'] = myFont

    if userConfig.returnDetailsInLogs() == True:
        debugLogsCheckbox.select()
        # global Debug.append_debug_details_to_logs
        Debug.append_debug_details_to_logs = True
    # debugLogsCheckbox.pack()
    debugLogsCheckbox.place(x=70, y=440)
    c3 = tkinter.Checkbutton(frame,
                             text='show debug details in cmd',
                             variable=var3,
                             onvalue=1,
                             offvalue=0,
                             background=main_collor_,
                             fg=GUI_VARS.TEXT_collor,
                             selectcolor="blue",
                             command=lambda: checkBoxAction_cmdDetails(str(var3.get())))
    c3['font'] = myFont
    if userConfig.details_in_cmd == True:
        c3.select()
        # global Debug.show_cmd_details
        Debug.show_cmd_details = True
    c3.place(x=70, y=470)  # c3.pack()


    #while(Debug_Options.Debug.run_gui):
    frame.mainloop()

    #a = input('Give mae number')

    # if downloading_thread.is_alive():
    #    downloading_thread.join() # wait until thread is executed

    return 0