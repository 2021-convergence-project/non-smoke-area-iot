from mqtt import add_topic_handler
import io
from pydub import AudioSegment
from pydub.playback import play
import requests
import threading
import paho.mqtt.client as mqtt
from time import sleep

URL = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
HEADERS = {
    "Content-Type" : "application/xml",
    "Authorization" : "KakaoAK c7ad259e95ebd7a313853e56601b000c"
}

state = False

def synthesize(text):
    DATA = f"""
    <speak>
        <voice name="WOMAN_DIALOG_BRIGHT">
            {text}
        </voice>
    </speak>"""
    res = requests.post (URL, headers = HEADERS, data = DATA.encode ('utf 8'))
    if res.status_code == 200:
        return res.content
    else:
        print(res.status_code,res.text)

def play_audio(audio):
    sound = io.BytesIO(audio)
    song = AudioSegment.from_mp3(sound)
    play(song)

def play_default():
    text = '이 곳은 이 곳은 금연 구역 입니다.'
    audio = synthesize(text)
    play_audio(audio)


def speaker():
    global state
    while True:
        if state:
            print('시작')
            play_default()
            sleep(5)
            print('종료')
            state = False
        # else:
            # print('종료')
        sleep(1)

def speaker_state(topic,value):
    global state
    state = value

add_topic_handler('smoke/signal',speaker_state)


my_thread = threading.Thread(target=speaker)
my_thread.start()

