import whisper
import time

class VideoContentSearch:
    def __init__(self, src):
        self.model = whisper.load_model("base")
        # TODO:
        #   - extract audio from video
        self.audio = whisper.load_audio(src)

        # TODO: link from youtube or local (uploaded video)

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

        return result
