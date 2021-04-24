# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:53:36 2021

@author: hh026
"""

from flask import Flask, render_template, Response
import cv2
import threading
from space_classification import Space_classification
import tensorflow as tf
import numpy as np
from PyQt5 import QtWidgets


class Stream:
       
    app = Flask(__name__)
    
    def init_stream(Window, videosource, scale, frame, name):   #init
        global model, point_list, cap, outputFrame, lock, count, result_text, MainWindow, video_scale, video_frame, park_name
        
        MainWindow = Window        
        error_code = Space_classification.checkfile()
        
        if error_code == 0:   #학습모델
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no trained model file.") 
            return
        if error_code == 1:   #좌표파일없음
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no point lists file.")  
            return
            
        cap = cv2.VideoCapture(videosource)
        
        if not cap.isOpened():   #url주소
            QtWidgets.QMessageBox.warning(MainWindow, "Load failed", "Failed to load video(Invalid url address)") 
            cap.release()
            return
        
        outputFrame = None    
        lock = threading.Lock()
        

        #저장된 좌표 불러오기
        point_list = []
        point_list = Space_classification.list_point()   
        #저장된 모델 불러오기
        model = tf.keras.models.load_model('parking_model.h5')

        count = 0   
        result_text = ""
        park_name = name        
        video_scale = scale
        video_frame = frame
        t = threading.Thread(target=Stream.detect_motion)
        t.daemon = True
        t.start()
        Stream.app.run(host= '0.0.0.0', threaded=True)
        cap.release()
        cv2.destroyAllWindows()
        
        
    def detect_motion():
        global model, point_list, cap, outputFrame, lock, count, result_text, MainWindow, video_scale, video_frame
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * video_scale) #3
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * video_scale) #4
        
        while True:
            
            ret, frame = cap.read()            
            count += 1
            
            if ret == False:
                cap.release()
                break
            
            frame = cv2.resize(frame, (width, height))
            
            if count == video_frame:                
                frame, result_text = Space_classification.classification(frame, point_list, model)        
                with lock:    
                    count = 0
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
        return render_template('test.html', text = result_text , name = park_name)
    
if __name__ == '__main__':
    
    Stream.stream_video("./video.h264")    


    