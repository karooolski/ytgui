#from Utils import *

import os
from datetime import datetime
from StringManipulation import *
import time  # sleep
#from Utils import *
from Debug_Options import *
class Log_list:
    logs = []

def clear_logs():
    Log_list.logs.clear()

# reuturns file name for a log file (current time as a filename)
def log_filename():
    now = datetime.now()
    date_time = now.strftime("%Y %m %d")
    return date_time

def log_time():
    now = datetime.now()
    date_time = now.strftime("%Y %m %d, %H %M %S")
    return date_time


def warning(infos : str):
    print(bcolors.WARNING + "[WARNING] " + infos + bcolors.ENDC)
    log("[Warning] "+infos, hidden=True)

# OKCYAN
def info(infos: str):
    print(bcolors.OKCYAN + "[INFO] " + infos + bcolors.ENDC)  # for user during downloading
    try:
        Log_list.logs.append(remove_non_ascii("[INFO] " + infos) + "\n")
    except:
        print(bcolors.WARNING + "ERORR: log(): adding to logs list error" + bcolors.ENDC)


def log(message: str, hidden=False):
    if hidden == False:
        print(f"[Log] {message}")  # for user during downloading
    try:
        #Log_list.logs.append(remove_non_ascii(message) + "\n")
        make_log(remove_non_ascii(message), "[Log]")
    except:
        errorLog("log(): adding to logs list error")
        # print(bcolors.WARNING + "ERORR:  + bcolors.ENDC)


def errorLog(message: str):
    print(bcolors.WARNING + "[Error] " + message + bcolors.ENDC)  # for user during downloading
    try:
        #Log_list.logs.append(remove_non_ascii("[Error] " + infos) + "\n")
        make_log(message, "[Error]")
    except:
        print(bcolors.WARNING + "ERORR: log(): adding to logs list error" + bcolors.ENDC)


# dont show log info during downloading in cmd, but store it in log file
def hiddenlog(message: str):
    try:
        #Log_list.logs.append(remove_non_ascii(infos) + "\n")
        make_log(message, "[HLog]")
    except:
        print(bcolors.WARNING + "ERORR: hiddenlog(): adding to logs list error" + bcolors.ENDC)


# for additional log infos
def debuglog(message: str):
    append = Debug.append_debug_details_to_logs
    show = Debug.show_cmd_details
    if (append and show):
        print(f"[Debug] {message}")
        log(message)
    elif (append and not show):
        hiddenlog("[Debug]: " + message)
    elif (show and not append):
        print("[Debug]: " + message)


# (debug) print additional information in cmd
# for masive infos
def detail(*infos):
    if Debug.show_cmd_details == True:
        for info in infos:
            print(info)


def make_log(message : str, log_type : str):
    if Debug.make_logs == False:
        return
    time = log_time()
    try:
        logfilename = log_filename()
        file = open("logs/" + logfilename + ".txt", "a")
        file.write(f"{time} {log_type} {message} \n")
        file.close()
    except FileNotFoundError:
        os.makedirs("logs")
        make_log(message,log_type)
    except:
        errorLog("make_log(): some problem occured!")
