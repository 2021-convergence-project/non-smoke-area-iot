import paho.mqtt.client as mqtt
from mqtt import topicHandler
from . import devices
from cctv.main import ct

def on_connect(client, userdata, flags,rc):
    print("Connected with result code " + str(rc))
    if rc==0:
        client.subscribe("smoke/signal")
    else:
        print('연결실패 :',rc)


def on_message(client,userdata,msg):
    
    topic = '/'.join(msg.topic.split('/'))
    handler = topicHandler.get(topic)
    # print(topic)
    if handler:
        value = msg.payload.decode()
        print(topic,value)
        value = True if value=='1' else False
        
        handler(msg.topic, value)
    else:
        print('unknon topic',msg.topic)
    ct.state = True

mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
try :
    # mqttClient.connect("18.180.148.242",port=5555)
    mqttClient.connect("192.168.35.129")
    # mqttClient.connect("192.168.0.16")
    mqttClient.loop_start()     # 새로운 스레드로 이벤트 루프 실행, forever하면 웹서버 종료
except Exception as err:
    print('에러: %s'%err)    


