from pytube import YouTube # 19.07.2022 22:39
  
SAVE_PATH = "/home/karol/Pulpit/yt" # where to save 

# exemple
link= [ "https://www.youtube.com/watch?v=yXMob8_ygGo", "https://www.youtube.com/watch?v=N-HKIZd3vx4" ] 
  
for i in link:
    try: 
        yt = YouTube(i) 
    except: 
        print("Connection Error") #to handle exception 
    try: 
        yt.streams.get_audio_only("mp4").download(SAVE_PATH)
    except: 
        print("Some Error!") 
    print('Task Completed!') 
