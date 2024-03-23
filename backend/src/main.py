from __future__ import unicode_literals

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import utils
from search import MediaContentSearch

app = FastAPI()

# TODO: setup properly
origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
)

#app.mount('/frontend', StaticFiles(directory='frontend'), name='frontend')

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/load")
async def load(link):
    """
    Extract audio from a youtube video and get its transcript.
    """
    result = {}
    video = MediaContentSearch(link)
    #video.get_lang()
    transcript = video.get_transcript()

    for segment in transcript["segments"]:
        result[round(segment['start'], 2)] = segment['text']

    return result

# TODO
@app.get("/upload")
async def upload():
    return
