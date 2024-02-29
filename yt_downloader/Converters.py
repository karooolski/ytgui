import ffmpeg
# Convert mp4 -> mp3 ------------------------------------
from moviepy.audio.io import AudioFileClip
from moviepy.audio.AudioClip import *  # write_audiofile
from moviepy.audio.io.AudioFileClip import *  # close

from Logs import *
from Utils import *


# usage: downloading mp3
# Use moviepy to convert an mp4 to an mp3 with metadata support. Delete mp4 afterwards

def convert_to_mp3_with_metadata(file_path, deleteFile=True):
    func_title = "convert_to_mp3_with_metadata"
    debuglog(func_title + "start, got: ")
    try:
        debuglog(file_path)
    except:
        view = remove_non_ascii(file_path)
        debuglog("ASCI REMOVED : " + view)

    try:
        audio_clip = AudioFileClip(file_path);
        debuglog("Created AudioFileClip")
        file_path = file_path.replace("mp4", "mp3");
        debuglog("new filepath")
        audio_clip.write_audiofile(file_path);
        debuglog("AudioFile writed")
        audio_clip.close();
        debuglog("Audioclip closed")
        if deleteFile is True:
            os.remove(file_path.replace("mp3", "mp4"));
        debuglog("Removed Mp4 file")  # remove mp4 file
        # return file_path
        return True
    except:
        errorLog("[convert_to_mp3_with_metadata] Some problem occured during converting mp4 to mp3!")
        return False


# Usage: download video in 1080p and merge with audio
def merge_video_with_audio(SAVE_PATH):
    try:
        audio_path = SAVE_PATH + '/' + "videomerge.mp4"
        video_path = SAVE_PATH + '/' + "audiomerge.mp4"
        merged_video_path = SAVE_PATH + "/" + "output" + ".mp4"
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(audio_path)
        ffmpeg.output(audio, video, merged_video_path).run(overwrite_output=True)
        remove_file(SAVE_PATH, "videomerge.mp4")
        remove_file(SAVE_PATH, "audiomerge.mp4")
        log("Merge ended successfully")
    except:
        errorLog("Error: merge_video_with_audio(): Merge failed")
