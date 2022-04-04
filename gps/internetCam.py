# main.py# import the necessary packages
import time
from flask import Flask, render_template, Response
# import the necessary packages
import cv2
import threading
import sys

theCam = None

t = None
hasRun = False

ds_factor=0.6
class VideoCamera(object):
    def get_frame(self):
        #extracting frames
        frame = theCam.getFrame()
        if (len(frame) != 0):
            frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,
            interpolation=cv2.INTER_AREA)                    
            # gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            # face_rects=face_cascade.detectMultiScale(gray,1.3,5)
            # for (x,y,w,h) in face_rects:
            #  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #  break        # encode OpenCV raw frame to jpg and displaying it
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        ret, jpeg = cv2.imencode('.jpg', [])
        return jpeg.tobytes()


app = Flask(__name__)

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')

def gen(camera):
    while True:
        #get camera frame
        frame = None
        while (frame == None):
            frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def camLoop(nothing=None):
    while (True):
        theCam.tick()
        theCam.getCameraData()

def exit():
    t.terminate()
    t.join()

def run():
    global hasRun
    if (hasRun):
        return
    hasRun = True
    t = threading.Thread(target=lambda: app.run(host='0.0.0.0',port='5000'))
    t.start()

if __name__ == '__main__':
    from camera import Camera
    theCam = Camera(1, "Internet", "main")

    run()

    camLoop()
    # time.sleep(10)
    # defining server ip address and port
