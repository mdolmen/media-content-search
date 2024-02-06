from fastapi import FastAPI

import utils
from search import VideoContentSearch

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/transcript")
async def transcript():
    video = VideoContentSearch("testdata/c-in-100-seconds.opus")
    video.get_lang()

    transcript = video.get_transcript()
    result = {}
    for segment in transcript["segments"]:
        result[utils.float_to_datetime(segment['start'])] = segment['text']

    return result
