#2022 10 14 14 08
# EDIT METADATA of the file -----------------------------
# Convert mp4 -> mp3 ------------------------------------
from moviepy.audio.io import AudioFileClip
from moviepy.audio.AudioClip import *  # write_audiofile
from moviepy.audio.io.AudioFileClip import * # close
# import os 
def convert_to_mp3_with_metadata(file_path: str) -> str:
    try:
        # Use moviepy to convert an mp4 to an mp3 with metadata support. Delete mp4 afterwards
        try:
            audio_clip = AudioFileClip(file_path)
            try:
                file_path = file_path.replace("mp4", "mp3")
                audio_clip.write_audiofile(file_path)
                audio_clip.close()
                #try: # if you want to replace the old file than uncomment
                    #os.remove(file_path.replace("mp3", "mp4")) # remove mp4 file
                 #   return file_path
                #except: print("couldnt remove mp4 temporary file")
            except: print("couldnt write and close audiofile")
        except: print("couldnt make AdioFileClip")
    except:
        print("convert_to_mp3_with_metadata function error!")

# def gui(): # not yet

def main():
    mp4_path = "C:/Data/Music" # example: C:/Data/Music 
    filename = "filename.mp4"
    file_path = os.path.join(mp4_path, filename)
    final_file = convert_to_mp3_with_metadata(file_path)

main()