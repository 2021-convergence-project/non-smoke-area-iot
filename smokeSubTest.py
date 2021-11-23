import paho.mqtt.client as mqtt
import numpy as np
import cv2
import json
import base64

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if rc == 0:
        client.subscribe("smoke/mqtt")   # 연결 성공시 토픽 구독 신청
    else:
        print('연결실패: ',rc)

count = 1
def on_message(client, userdata, msg):

    # print(msg.topic)
    # print(msg.payload[:30])
    # print(type(msg.payload))

    payload = json.loads(msg.payload)
    print(payload['latitude'],payload['longitude'],payload['time'])
    img = payload['image']
    # img_ecd = img.encode('utf-8')
    # print(img[:30],img[-30:],img[-1])
    # print(img_ecd[:30])
    # print(type(img),type(img_ecd))
    
    # en_img = img.encode('utf-8')
    # print(en_img[:30])
    # print(type(msg.payload[:40]))
    global count
    f = open(f'./img/output_{count}.jpg','wb')
    f.write(base64.b64decode(img))
    f.close()
    count +=1



# 1. MQTT 클라이언트 객체 인스턴스화
client = mqtt.Client()

# 2. 관련 이벤트에 대한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

try:
    # 3. 브로커 연결
    client.connect("localhost")

    # 4. 메시지 루프 - 이벤트 발생시 해당 콜백 함수 호출
    client.loop_forever()
    
except Exception as err:
    print("에러 : %s"%err)
