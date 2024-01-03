import os
import threading
import pyaudio
from openai import OpenAI
from pygame import mixer
from pynput import keyboard as kb
import wave


client = OpenAI(api_key="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")
KEY = kb.Key.ctrl_l
FILE_PATH = 'audioFile/audioFile.wav'

# Audio recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

frames = []
is_recording = False

p = None
stream = None

def write_to_file(frames):
    wf = wave.open(FILE_PATH, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def record_audio():
    global is_recording, frames, p, stream
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)

def on_press(key):
    global is_recording, frames, p, stream
    if key == KEY and not is_recording:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        is_recording = True
        print('Recording started...')

        # Start a new thread to record audio
        threading.Thread(target=record_audio).start()

def on_release(key):
    global is_recording, frames, p, stream
    if key == KEY:
        is_recording = False
        print('Recording stopped.')
        # Write to file and close the stream
        write_to_file(frames)
        stream.stop_stream()
        stream.close()
        p.terminate() # Terminate the pyAudio Object
        text = speechToText()
        answer = chatGPT(text)
        textToSpeech(answer)
        playAudio()
        while mixer.music.get_busy(): pass
        # unload the loaded music file
        mixer.music.unload()

        os.remove('audioFile/output.mp3')



def speechToText():
    audio_file = open("audioFile/audioFile.wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    print(transcript)
    return transcript


def textToSpeech(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text,
    )

    response.stream_to_file("audioFile/output.mp3")
    print("audio file created")


def chatGPT(question):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant named jarvis that always refer to me as Mr. Stark, "
                           "you are specialized in answering questions based on truth and be concise to minimize your "
                           "answer length. If you do not know,"
                           "specify that you are not sure and give a certainty percentage of your answer when not "
                           "sure ",
            },
            {"role": "user", "content": question},
        ])
    answer = completion.choices[0].message.content
    print(answer)
    return answer


def playAudio():
    mixer.init()
    mixer.music.load("audioFile/output.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()


# Listener for key press and release
with kb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
