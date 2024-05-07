import os
import replicate

def transcribe(filename):
    """
    Run the whisper model on Replicate's hardware.

    filename: path to the local audio file to transcribe

    Returns the transcription result.
    """
    # TODO: get api from config.yaml (passed as arg)
    api = ""
    os.environ["REPLICATE_API_TOKEN"] = api

    result = []

    # When giving a local file, the lib will handle the upload. Use that for
    # now. We'll add the possibility to upload to a cloud storage (e.g. gdrive)
    # if necessary.
    audio_file = open(filename, "rb")

    output = replicate.run(
        "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
        input={
            "audio": audio_file,
            "model": "large-v3",
            "language": "en",
            "translate": False,
            "temperature": 0,
            "transcription": "plain text",
            "suppress_tokens": "-1",
            "logprob_threshold": -1,
            "no_speech_threshold": 0.6,
            "condition_on_previous_text": True,
            "compression_ratio_threshold": 2.4,
            "temperature_increment_on_fallback": 0.2
        }
    )
    print(output)
    
    # Build array of segments
    for segment in output['segments']:
        result.append((segment['start'], segment['text']))

    return result
