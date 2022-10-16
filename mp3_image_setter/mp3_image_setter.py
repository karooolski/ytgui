#2022 10 14 21 00
# EDIT METADATA of the file -----------------------------
import eyed3
from eyed3.id3.frames import ImageFrame
#from eyed3.id3 import tag
import eyed3.id3 as id3
import os 

# you have to have file named thumbnail.jpg in the SAVE_PATH location

def main():
    # using windows remember to change "\" to "/" right here: 
    SAVE_PATH = ""
    audio_path = "" # same as SAVE_PATH but with name of music with .mp3 ending
    audiofile = eyed3.load(audio_path)
    if not audiofile.tag:
        audiofile.initTag()
    try:    
        tag = id3.Tag()
        tag.parse(audio_path)
        tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(SAVE_PATH,'thumbnail.jpg'),'rb').read(), 'image/jpeg')
        tag.save(version=eyed3.id3.ID3_V2_3)
    except: print("can not set an image!")
    
main()
