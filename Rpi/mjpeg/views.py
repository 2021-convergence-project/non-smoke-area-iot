from mysite.picam import MJpegStreamCam
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, StreamingHttpResponse
import time
from datetime import datetime
import os
from mysite.settings import BASE_DIR
import mjpeg.sensors

mjpegstream = MJpegStreamCam()
SNAPSHOT_DIR = os.path.join(BASE_DIR,"media/snapshot/")

def save_image(image):
    now = datetime.now()
    fname = now.strftime("snapshots_%Y%m%d_%H%M%S.jpg")
    file_path = os.path.join(SNAPSHOT_DIR,fname)
    with open(file_path,'wb') as f:
        f.write(image)

def get_snapshot_history():
    files = os.listdir(SNAPSHOT_DIR)
    files.sort(reverse=True)
    return files

class CamView(TemplateView):
    template_name = "cam.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["mode"] = self.request.GET.get("mode","#")
        context["snapshots"] = get_snapshot_history()
        return context

def snapshot(request):
    time.sleep(0.3)  # stream 중단시 정리 시간을 둠
    image = mjpegstream.snapshot()
    save_image(image)
    return HttpResponse(image,content_type="image/jpeg")

def mjpeg_stream(request):
    time.sleep(0.3)
    return StreamingHttpResponse(mjpegstream,
        content_type='multipart/x-mixed-replace;boundary=--myboundary')

