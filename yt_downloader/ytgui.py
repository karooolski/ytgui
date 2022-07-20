import tkinter as tk # 20.07.2022
from pytube import YouTube 
#https://www.geeksforgeeks.org/how-to-get-the-input-from-tkinter-text-box/

# this program also need '/' slashes in the path like in linux instead "\"
def change_backslashes(word):
    ex = '\\'
    l = list(word)
    for i in range(len(word)):
        #w = print(word[i])
        if l[i] == ex:
            l[i] = '/'
        s = ''.join(l)
    return(s)

# Top level window
frame = tk.Tk()
frame.title("TextBox Input")
frame.geometry('500x300')

#global path_confirm
#path_confirm = 0

global SAVE_PATH
SAVE_PATH = ""
global link 
link = ""

def printInput():
   
   #global path_confirm
    
    inp = inputtxt.get(1.0, "end-1c")
    global SAVE_PATH
    SAVE_PATH = inp
    SAVE_PATH = change_backslashes(SAVE_PATH)
    l = lbl.config(text = "Provided Input: "+inp)
    print(inp)
    
    
def printInput2():
    # print(path_confirm)
   # if path_confirm == 1 : 
    inpp = input2txt.get(1.0, "end-1c")
    global SAVE_PATH
    global link 
    link = inpp
    p = lbll.config(text = "Provided Input: "+inpp)  
    print(inpp)
    print("Try download a video")
    print("link: "+link)
    print("SAVE_PATH: "+SAVE_PATH)

    try: 
        yt = YouTube(link) 
    except: 
        print("Connection Error") #to handle exception 
    try: 
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(SAVE_PATH)
    except: 
        print("Some Error!") 
    print('Task Completed!') 
    #else: 
    #p = lbll.config(text="Nie wprowadzono sciezki")
    #print("nie wprowadzono sciezki")
  
# TextBox Creation
inputtxt = tk.Text(frame,height = 5,width = 20)
inputtxt.pack()
# Button Creation
printButton = tk.Button(frame,text = "sciezka_zatwierdz", command = printInput)
printButton.pack()
# Label Creation
lbl = tk.Label(frame, text = "")
lbl.pack()

input2txt = tk.Text(frame,height = 5,width = 20)  
input2txt.pack()
print2Button = tk.Button(frame,text = "link_zatwierdz", command = printInput2)
print2Button.pack()
lbll = tk.Label(frame,text="")
lbll.pack()



frame.mainloop()



#SAVE_PATH = "" # where to save #/home/karol/Pulpit/yt
