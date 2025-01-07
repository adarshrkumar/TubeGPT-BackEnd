import os.path

from pytube import YouTube
from moviepy.editor import *

from openai import OpenAI
client = OpenAI()

from fastapi import FastAPI, Request
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/videos/{video_id}')
def host_video(video_id: str): 
    if os.path.isfile(f'./videos/{video_id}.mp4'): 
        return {"hasVideo": True}
    else: 
        return {"hasVideo": False}

@app.get('/audio/{video_id}')
def host_audio(video_id: str): 
    if os.path.isfile(f'./audio/{video_id}.mp3'): 
        return {"hasAudio": True}
    else: 
        return {"hasAudio": False}

@app.get("/getTranscript")
def read_item(request: Request):
    params = request.query_params
    video_id = params['id']
    transcript = transcribeVideo(video_id)
    return {"video_id": video_id, "transcript": transcript.text}


def downloadAudio(video_id: str): 
    if not os.path.isfile(f'./audios/{video_id}.mp3'):
        yt = YouTube(f'https://youtube.com/watch?v={video_id}')
        vid = yt.streams.get_audio_only()
        print(vid)
        vid.download(output_path='./audios/',filename=f'{video_id}.mp3')

    return f'./videos/{video_id}.mp3'

def convertToAudio(video_id: str):
    if not os.path.isfile(f'./audios/{video_id}.mp3'):
        downloadVideo(video_id)
        FILETOCONVERT = AudioFileClip(f'./videos/{video_id}.mp4')
        FILETOCONVERT.write_audiofile(f'./audios/{video_id}.mp3')
        FILETOCONVERT.close()
    return f'./audios/{video_id}.mp3'

def transcribeVideo(video_id: str):
    video_path = downloadAudio(video_id)
    
    audio_file = open(video_path, "rb")
    transcript = client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file
    )
    return transcript