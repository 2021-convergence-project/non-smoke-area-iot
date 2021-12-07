topicHandler = {}   # '토픽명' : 핸들러 함수 쌍 관리 시전

def add_topic_handler(topic,handler):
    global topicHandler
    topicHandler[topic] = handler