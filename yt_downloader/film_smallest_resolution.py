# importing the module 
from pytube import YouTube 
  
SAVE_PATH = "/home/karol/Pulpit/yt" # where to save 

link="https://www.youtube.com/watch?v=yXMob8_ygGo"
  
try: 
    yt = YouTube(link) 
except: 
    print("Connection Error") #to handle exception 
try: 
    stream = yt.streams.first()
    stream.download(SAVE_PATH)
except: 
    print("Some Error!") 
print('Task Completed!') 
