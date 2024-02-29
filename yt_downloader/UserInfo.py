from sqlitedict import SqliteDict  # simple database for storing user options locally: -----------------
from Logs import *
class UserConfig():
    link = ""
    SAVE_PATH = " "
    allow_logs = False
    details_in_cmd = False
    details_in_loggs = False
    last_combobox_state = 0

    # default configuration
    def __init__(self):
        self.link = ""
        self.SAVE_PATH = ""
        self.allow_logs = False
        self.details_in_cmd = False
        self.details_in_loggs = False
        self.last_combobox_state = 0

    # @staticmethod
    def saveConfiguration(self, key, value):  # save object with user configuration to existing cache file
        cache_file = "cache.sqlite3"
        try:
            with SqliteDict(cache_file) as mydict:
                mydict[key] = value  # Using dict[key] to store
                mydict.commit()  # Need to commit() to actually flush the data
        except Exception as ex:
            print("Error during storing data (Possibly unsupported):", ex)

    # @staticmethod
    def loadConfiguration(self, key):
        cache_file = "cache.sqlite3"
        try:
            with SqliteDict(cache_file) as mydict:
                object_ = mydict[key]  # No need to use commit(), since we are only loading data!
            return object_
        except Exception as ex:
            debuglog("Creating new user configuration file :")
            object_ = UserConfig()  # make new default config file if it didnt exist
            object_.saveConfiguration(key, object_)
            return object_  # mydict[key]

    def returnDetailsInLogs(self):
        return self.details_in_loggs
