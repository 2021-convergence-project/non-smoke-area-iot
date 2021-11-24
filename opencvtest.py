from datetime import datetime
from time import sleep
import numpy as np
import cv2
import paho.mqtt.client as mqtt
import io
import json
import base64

print('test1')
mc = mqtt.Client()
mc.connect("18.180.148.242",port=5555)
print('test2')
count = 1

cap = cv2.VideoCapture(0)   # 1번 카메라


cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
cap.set(cv2.CAP_PROP_FPS,5)

lat = 37.5683
lon = 126.9778
while True:
    if datetime.now().second == 0 or datetime.now().second == 30:
        # 프레임 캡처
        while True:
            retval, frame = cap.read()  # retval : T/F , frame : 영상(numpy)배열
            if not retval: break
            
            # cv2.imwrite(f'./img/mqtt_test_{count}.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY, 20])

            print(count)
            # print(frame.shape)
            now = datetime.now()
            print(str(now))


            img_path = f'./mqttimg/mqtt_test{count}.jpg'
            print(img_path)

            cv2.imwrite(img_path,frame)
            count += 1
            cv2.imshow('frame',frame)

            f= open(img_path,'rb')
            fdata = f.read()
            fary = bytearray(fdata)
            # print(fdata[:30])

            byteArr = base64.b64encode(fdata)

            str_img = byteArr.decode('utf-8')
            
            
            # print(str_img.encode('utf-8')[:30])
            
            # mc.publish('smoke/test',fary)

            mqtt_msg = json.dumps( {"latitude":f"{lat}","longitude":f"{lon}","time":f"{str(now)}","image":str_img} )
            mc.publish('smoke/mqtt',mqtt_msg)


            key = cv2.waitKey(25)   # 초당 40프레임 처리
            if key == 27 or datetime.now().second == 5 or datetime.now().second == 35:
                cv2.destroyAllWindows()
                count = 1
                break    # ESC키를 누른경우  루프 탈출

