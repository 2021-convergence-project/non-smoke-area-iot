from datetime import datetime
from time import sleep
import cv2
import paho.mqtt.client as mqtt
import json
import base64
import serial
import pynmea2
from mjpeg.views import mjpegstream
import threading

class Cctv:
    def __init__(self):
        self.state = False

ct=Cctv()


def parseGPS(str):
    global lat,lon
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        if msg.lat:
            lat1,lat2,lat3 = int(msg.lat[:2]),int(msg.lat[2:4]),int(msg.lat[5:])/10000*60
            lat = round(lat1 + lat2/60 + lat3/3600,6)
            
        else: lat = ''
            
        if msg.lon:
            lon1,lon2,lon3 = int(msg.lon[:3]),int(msg.lon[3:5]),int(msg.lon[6:])/10000*60
            lon = round(lon1+ lon2/60 + lon3/3600,6)
        else: lon = ''

        # print(f"위도: {lat} 경도: {lon}")
        return [lat,lon]

serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)

lat,lon = [None,None]

mc = mqtt.Client()
# mc.connect("18.180.148.242",port=5555)
mc.connect("192.168.35.129")
# mc.connect("192.168.0.16")

count = 1

def capture(frame):
    global count
    frame = cv2.flip(frame, -1)
    print(count)
    now = datetime.now()
    print(str(now))
    print(lat,lon)

    img_path = f'/home/pi/workspace/nonsmoke/cctv/imgtest/mqtt_test{count}.jpg'
    print(img_path)

    cv2.imwrite(img_path,frame,[cv2.IMWRITE_JPEG_QUALITY, 50])
    count += 1
    cv2.imshow('frame',frame)
    return img_path,now


def pub_mqtt():
    global count
    first=False
    while True:
        ser = serialPort.readline()
        data = ser.decode()
        parseGPS(data)
        if (datetime.now().second == 0 and not first )  or ct.state:
            # 프레임 캡처
            while True:
                frame = mjpegstream.frame
                
                if frame is None:
                    break
                # print('test',ct.state)
                first = True
                img_path,now= capture(frame)

                # 이미지 파일 열기
                f= open(img_path,'rb')
                fdata = f.read()
                # base64로 인코딩
                byteArr = base64.b64encode(fdata)
                # 문자열 변환
                str_img = byteArr.decode('utf-8')
                # json에 담아 전송
                mqtt_msg = json.dumps( {"latitude":f"{lat}","longitude":f"{lon}","time":f"{str(now)}","image":str_img} )
                mc.publish('smoke/cctv',mqtt_msg)

                key = cv2.waitKey(25)   # 초당 40프레임 처리
                sleep(0.4)
                if key == 27 or count > 8:
                    cv2.destroyAllWindows()
                    count = 1
                    ct.state = False
                    break    # ESC키를 누른경우  루프 탈출

my_thread2 = threading.Thread(target=pub_mqtt)
my_thread2.start()