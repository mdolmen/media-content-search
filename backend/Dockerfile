FROM debian:latest

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN apt update && apt install -y ffmpeg git gcc python3 python3-pip python3-venv
RUN python3 -m pip install -r requirements.txt --break-system-packages
RUN python3 -m pip install git+https://github.com/openai/whisper.git --break-system-packages

COPY src .
