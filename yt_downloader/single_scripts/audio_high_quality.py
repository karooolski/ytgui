from pytube import YouTube # 19.07.2022 22:26
  
SAVE_PATH = "/home/karol/Pulpit/yt" # where to save 

link="https://www.youtube.com/watch?v=yXMob8_ygGo"
  
try: 
    yt = YouTube(link) 
except: 
    print("Connection Error") #to handle exception 
try: 
    yt.streams.get_audio_only("mp4").download(SAVE_PATH)
except: 
    print("Some Error!") 
print('Task Completed!') 
