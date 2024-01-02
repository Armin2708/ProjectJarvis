import pyaudio
import wave
from pynput import keyboard as kb
from openai import OpenAI
from pygame import mixer


client = OpenAI(api_key="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")

# Set key to be pressed
KEY = kb.Key.cmd_r
# Set your desired file path
FILE_PATH = 'audioFile/audioFile.wav'
# Audio recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

frames = []
is_recording = False

# Start PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)



def transcription():
    audio_file = open(FILE_PATH, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript


def answer(transcript):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant named jarvis that always refer to me as master Armin, "
                           "you are specialized in answering questions based on truth. If you do not know, "
                           "specify that you are not sure and give a certainty percentage of your answer when not "
                           "sure ",
            },
            {"role": "user", "content": transcript},
        ])
    answer = completion.choices[0].message.content
    return answer


def speak(answer):
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=answer,
    )
    response.stream_to_file("audioFile/output.mp3")
    print("done")


def playAudio():
    # Starting the mixer
    mixer.init()
    # Loading the song
    mixer.music.load("audioFile/output.mp3")
    # Setting the volume
    mixer.music.set_volume(0.7)
    # Start playing the song
    mixer.music.play()


def write_to_file(frames):
    wf = wave.open(FILE_PATH, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def on_press(key):
    global is_recording, frames
    if key == KEY:
        frames = []  # Clear the frames
        is_recording = True
        print("Recording started...")


def on_release(key):
    global is_recording, frames
    if key == KEY:
        is_recording = False
        print("Recording stopped.")
        # Write to file and close the stream
        write_to_file(frames)
        stream.stop_stream()
        stream.close()
        transcript = transcription()
        ans = answer(transcript)
        speak(ans)
        playAudio()


# Listener for key press and release
listener = kb.Listener(on_press=on_press, on_release=on_release)
listener.start()  # Removed listener.join() and added listener.start()

while True:  # Loop to keep the program running
    if is_recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)