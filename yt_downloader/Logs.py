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
    date_time = now.strftime("%Y %m %d, %H %M %S")
    return date_time


def warning(infos : str):
    print(bcolors.WARNING + "[WARNING] " + infos + bcolors.ENDC)
    log(infos, hidden=True)

# OKCYAN
def info(infos: str):
    print(bcolors.OKCYAN + "[INFO] " + infos + bcolors.ENDC)  # for user during downloading
    try:
        Log_list.logs.append(remove_non_ascii("[INFO] " + infos) + "\n")
    except:
        print(bcolors.WARNING + "ERORR: log(): adding to logs list error" + bcolors.ENDC)


def log(infos: str, hidden=False):
    if hidden == False:
        print(infos)  # for user during downloading
    try:
        Log_list.logs.append(remove_non_ascii(infos) + "\n")
    except:
        errorLog("log(): adding to logs list error")
        # print(bcolors.WARNING + "ERORR:  + bcolors.ENDC)


def errorLog(infos: str):
    print(bcolors.WARNING + "[Error] " + infos + bcolors.ENDC)  # for user during downloading
    try:
        Log_list.logs.append(remove_non_ascii("[Error] " + infos) + "\n")
    except:
        print(bcolors.WARNING + "ERORR: log(): adding to logs list error" + bcolors.ENDC)


# dont show log info during downloading in cmd, but store it in log file
def hiddenlog(infos: str):
    try:
        Log_list.logs.append(remove_non_ascii(infos) + "\n")
    except:
        print(bcolors.WARNING + "ERORR: hiddenlog(): adding to logs list error" + bcolors.ENDC)


# for additional log infos
def debuglog(infos: str):
    append = Debug.append_debug_details_to_logs
    show = Debug.show_cmd_details
    if (append and show):
        log("[debug]: " + infos)
    elif (append and not show):
        hiddenlog("[debug]: " + infos)
    elif (show and not append):
        print("[debug]: " + infos)


# (debug) print additional information in cmd
# for masive infos
def detail(*infos):
    if Debug.show_cmd_details == True:
        for info in infos:
            print(info)


def make_log(logs: list):
    if Debug.make_logs == False:
        return
    try:
        logfilename = log_filename()
        file = open("logs/" + logfilename + ".txt", "w")
        for i in range(len(logs)):
            file.write(str(logs[i]))
        file.close()
    except FileNotFoundError:
        os.makedirs("logs")
        make_log(logs)
    except:
        errorLog("make_log(): some problem occured!")
