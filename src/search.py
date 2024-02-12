import whisper
import time
import yt_dlp
import glob
import os

class VideoContentSearch:
    def __init__(self, link):
        self.prefix = "/tmp/vcs_"
        self.count_tmpfiles = 0
        self.model = whisper.load_model("base")
        self.src = self.extract_audio(link)
        self.audio = whisper.load_audio(self.src)

        # TODO: link from youtube or local (uploaded video)

    def extract_audio(self, link):
        ret = 0
        result = {}
        src = ""
        video_id = ""
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'outtmpl': '/tmp/vcs_%(id)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            video_id = info["id"]
            ret = ydl.download(link)

        if ret == 0:
            print("load OK")
            src = glob.glob(f"{self.prefix}{video_id}*")[0]

        return src

    def get_lang(self):
        extract = whisper.pad_or_trim(self.audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(extract).to(self.model.device)

        # detect the spoken language
        _, probs = self.model.detect_language(mel)
        lang = max(probs, key=probs.get)
        print(f"[+] Detected language: {lang}")

        return lang

    def get_transcript(self):
        start = time.time()
        result = self.model.transcribe(self.audio);
        end = time.time()
        print(f"[+] Transcribe time = {end-start}")
        self.cleanup()

        return result

    def cleanup(self):
        """
        Remove downloaded files after a while.
        """
        self.count_tmpfiles += 1

        if self.count_tmpfiles < 10:
            return

        for f in glob.glob(f"{prefix}*"):
            os.remove(f)
        self.count_tmpfiles += 0
