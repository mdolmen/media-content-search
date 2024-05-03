import time
import yt_dlp
import glob
import os

def ytdl_and_extract_audio(link):
    """
    Download the video and extract the audio.

    Returns a link to the audio file on disk.
    """
    prefix = "/tmp/mcs_"
    ret = 0
    result = {}
    src = "nothing"
    video_id = ""
    ydl_opts = {
        'quiet': True,
        'no-progress': True,
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': '/tmp/mcs_%(id)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            video_id = info["id"]
            ret = ydl.download(link)
    except Exception as error:
        print(f"ERROR: {error}")
        ret = 1

    if ret == 0:
        print("load OK")
        src = glob.glob(f"{prefix}{video_id}*")[0]

    return src

def cleanup():
    """
    Remove downloaded files.
    """
    for f in glob.glob(f"{prefix}*"):
        os.remove(f)
