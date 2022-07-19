from pytube import YouTube 
  
SAVE_PATH = "/home/karol/Pulpit/yt" # where to save 

# exemple
link= [ "https://www.youtube.com/watch?v=yXMob8_ygGo", "https://www.youtube.com/watch?v=N-HKIZd3vx4" ] 
  
for i in link:
    try: 
        yt = YouTube(i) 
    except: 
        print("Connection Error") #to handle exception 
    try: 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
    except: 
        print("Some Error!") 
    print('Task Completed!') 