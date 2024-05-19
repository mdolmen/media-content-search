import os
import replicate
import subprocess

def get_gdrive_dl_link(link):
    """
    By default the gdrive link will lead to a preview of the file, the browser
    will try to open it and then propose to download the file if it fails).
    This function extract the file ID to build an alternative link that will
    directly trigger a download (no preview).
    """
    file_id = link[link.rfind('=')+1:]
    url_template = "https://drive.google.com/uc?export=download&id="

    return url_template + file_id

def transcribe(filename):
    """
    Run the whisper model on Replicate's hardware.

    filename: path to the local audio file to transcribe

    Returns the transcription result.
    """
    # TODO: get api from config.yaml (passed as arg)
    api = ""
    os.environ["REPLICATE_API_TOKEN"] = api
    remote_storage = "remote:mcs"

    result = []

    # Upload file to personal cloud storage
    subprocess.run(["rclone", "copy", filename, remote_storage])

    # Get public link for that file
    output = subprocess.run(
        ["rclone", "link",
         f"{remote_storage}/{filename[filename.rfind('/')+1:]}"],
        capture_output=True)
    public_link = get_gdrive_dl_link(output.stdout.rstrip().decode("utf-8"))

    output = replicate.run(
        "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
        input={
            "audio": public_link,
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
    
    # Build array of segments
    for segment in output['segments']:
        result.append((segment['start'], segment['text']))

    return result
