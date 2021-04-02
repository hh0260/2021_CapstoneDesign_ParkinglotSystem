# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:53:36 2021

@author: hh026
"""

from flask import Flask, render_template, Response
import cv2
import threading
from makevideo import MakeVideo
import tensorflow as tf
import numpy as np


class Stream:
       
    app = Flask(__name__)
    
    def stream_video(videosource):   #init
        global name, model, point_list, camera, outputFrame, lock, count, total_num, freespot_num, result_text

        camera = cv2.VideoCapture(videosource)    
        outputFrame = None    
        lock = threading.Lock()

        #저장된 좌표 불러오기
        point_list = []
        point_list = MakeVideo.list_point()   
        #저장된 모델 불러오기
        model = tf.keras.models.load_model('parking_model.h5')

        count = 0   
        freespot_num = 0   
        total_num = 0 
        result_text = ""
        name = "글로벌 평생 학습관"
        t = threading.Thread(target=Stream.detect_motion)
        t.daemon = True
        t.start()
        Stream.app.run(host = '0.0.0.0', threaded=True)


    def detect_motion():
        global name, model, point_list, camera, outputFrame, lock, count, total_num, freespot_num, result_text
        
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))//2 #3
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))//2 #4
        
        while True:
            success, frame = camera.read()            
            count += 1
            if not success:
                break
            frame = cv2.resize(frame, (width, height))
            if count == 3:
                cut = np.copy(frame)
            
                i=0
                while i < len(point_list)-3:   #모든 영역 빨간색
                    frame = MakeVideo.draw_poly(frame, point_list, i, [0, 0, 255])
                    i += 4 
                i=0
                while i < len(point_list)-3:
                    img = MakeVideo.warp_image(cut, point_list[i], point_list[i+1], 
                                  point_list[i+2], point_list[i+3])
            
                    img = tf.expand_dims(img, 0)
                    predictions = model.predict(img)
                    score = tf.nn.softmax(predictions[0])
            
                    total_num += 1
                    if np.argmax(score):
                        freespot_num += 1
                        frame = MakeVideo.draw_poly(frame, point_list, i, [0, 255, 0])
                    i += 4
        
        
            with lock:
                if count == 3:
                    result_text = str(freespot_num)  + "/"+ str(total_num)
                    count = 0
                    freespot_num = 0
                    total_num = 0 
                    cv2.putText(frame, result_text, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 6, cv2.LINE_AA)
                    outputFrame = np.copy(frame)
            
    def gen_frames():
        global outputFrame, lock
        while True:

            with lock:

                if outputFrame is None:
                    continue

                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

                if not flag:
                    continue

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(Stream.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=--frame')

    @app.route('/')
    def index():
        return render_template('test.html', text = result_text , name = name)
    
if __name__ == '__main__':
    
    Stream.stream_video("./video.h264")    


    