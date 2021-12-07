# from gpiozero import MotionSensor, LED, Button
from signal import pause
import requests
import json
import sounddevice as sd
import soundfile as sf
import io


# pir = MotionSensor(12)


def send_talk(message):
    print('지진발생 테스트')
    # 카톡 메시지 전송용 URL    
    talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    with open("access_token.txt", "r") as f:
        token = f.read()
    header = {"Authorization": f"Bearer {token}"}
    
    # 카톡 메시지 템플릿
    text_template = {
        'object_type': 'text',  # 템플릿 종류
        'text': message,
        'link': {
            'web_url': 'http://192.168.35.71:8000/mjpeg/?mode=stream',
            'mobile_web_url': 'http://192.168.35.71:8000/mjpeg/?mode=stream'
        },
        'button_title': '카메라 보기'
    }
    feed_template={
        "object_type": "feed",
        "content": {
            "title": message,
            'description': '지진이 발생되었습니다. 대피하세요',
            # "image_url": "http://kgrsys.com/wp-content/uploads/2017/01/page-icon061.jpg",
            # 지진 이미지
            "image_url": "https://static.vecteezy.com/system/resources/thumbnails/000/571/491/small/vector60-568-01.jpg",
            # "image_width": 640,
            # "image_height": 640,
            "link": {
                
                # 'web_url': 'http://192.168.35.71:8000/mjpeg/?mode=stream',
                # 'mobile_web_url': 'http://192.168.35.71:8000/mjpeg/?mode=stream'
                'web_url': 'https://www.weather.go.kr/pews/man/m1.html',
                'mobile_web_url': 'https://www.weather.go.kr/pews/man/m1.html'
            }
        },
        'button_title':'행동 요령'
    }

    # print(text_template)
    payload = {'template_object': json.dumps(feed_template)}
    res = requests.post(talk_url, data=payload, headers=header)
    return res


def detect():
    # 카톡 메시지 보내기
    send_talk('침입 발생')

print('test1')
# pir.when_motion = detect
