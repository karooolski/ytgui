from pytube import YouTube 
  
SAVE_PATH = "/home/karol/Pulpit/yt" # where to save 

link="https://www.youtube.com/watch?v=yXMob8_ygGo"
  
try: 
    yt = YouTube(link) 
except: 
    print("Connection Error") #to handle exception 
try: 
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
except: 
    print("Some Error!") 
print('Task Completed!') 
