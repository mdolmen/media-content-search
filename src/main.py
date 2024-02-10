from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import utils
from search import VideoContentSearch

app = FastAPI()

# TODO: setup properly
origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
)

#app.mount('/frontend', StaticFiles(directory='frontend'), name='frontend')

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/transcript")
async def transcript():
    video = VideoContentSearch("../testdata/c-in-100-seconds.opus")
    video.get_lang()

    transcript = video.get_transcript()
    result = {}
    for segment in transcript["segments"]:
        result[round(segment['start'], 2)] = segment['text']

    return result
