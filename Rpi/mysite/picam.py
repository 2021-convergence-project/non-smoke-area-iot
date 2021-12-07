from time import sleep
import cv2

img = None

class PiCam:
    def __init__(self, framerate=24, width=640, height=480):
        # self.size = (width, height)
        self.framerate = framerate

        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
        self.camera.set(cv2.CAP_PROP_FPS,framerate)
        self.frame = None

    # 사진 1장(jpeg) 리턴
    def snapshot(self):
        retval, self.frame = self.camera.read()
        r_frame = cv2.flip(self.frame, -1)
        ret,s_img = cv2.imencode('.jpg',r_frame)
        return s_img.tobytes()

class MJpegStreamCam(PiCam):
    def __init__(self, framerate=24, width=640, height=480):
        # self.frame = None
        super().__init__(framerate=framerate, width=width, height=height)
    
    def __iter__(self):
        global img
        while True:
            self.retval, self.frame = self.camera.read()
            r_frame = cv2.flip(self.frame, -1)
            
            ret,img = cv2.imencode('.jpg',r_frame)
            image = img.tobytes()
            # print(image[:50])
            
            # generator 생성
            yield(b'--myboundary\n' # 경계선
                    b'Content-Type:image/jpeg\n'
                    # f"{len(image)}" : 문자열, .encode() : 문자열 -> byte배열
                    b'Content-Length: '+ f"{len(image)}".encode() + b'\n'
                    b'\n'+image + b'\n')    #'\n' : 헤더 바디 구분 빈 줄
            