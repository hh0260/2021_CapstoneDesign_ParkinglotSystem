# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:26:25 2021

@author: hh026
"""
import cv2
import os
import sys
import numpy as np
import tensorflow as tf
import Makevideo
import Get_line

cap = cv2.VideoCapture("./video.h264")
#cap = cv2.VideoCapture("http://keycalendar.iptime.org:8091/?action=stream")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))//2 #3
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))//2 #4

#저장된 좌표 불러오기
#if not os.path.isfile('points.txt'):
if not os.path.isfile('cap.jpg'):
    print("학습모델 파일이 없습니다.")
    Get_line.MakeLine.capture(cap)
    
point_list = []
point_list = Makevideo.MakeVideo.list_point()     

#저장된 모델 불러오기
if not os.path.isfile('parking_model.h5'):
    print("학습모델 파일이 없습니다.")
    sys.exit()
    
model = tf.keras.models.load_model('parking_model.h5')

class_names = ['car','empty']
count = 0     
freespot_num = 0   
total_num = 0 

while (cap.isOpened):
    
    ret, frame = cap.read()
    count += 1
    if ret == False:
        break
    #frame = cv2.resize(frame, (width, height))
    if count == 1:
        count = 0
        cut = np.copy(frame)
        
        i=0
        while i < len(point_list)-3:   #모든 영역 빨간색
            frame = Makevideo.MakeVideo.draw_poly(frame, point_list, i, [0, 0, 255])
            i += 4      
        
        i=0
        while i < len(point_list)-3:
            img = Makevideo.MakeVideo.warp_image(cut, point_list[i], point_list[i+1], 
                              point_list[i+2], point_list[i+3])
            
            img = tf.expand_dims(img, 0)
            predictions = model.predict(img)
            score = tf.nn.softmax(predictions[0])
            
            print(str(total_num)+": "+class_names[np.argmax(score)]+", "+str(100 * np.max(score)))
            total_num += 1
            if np.argmax(score):
                frame = Makevideo.MakeVideo.draw_poly(frame, point_list, i, [0, 255, 0])
                
            i += 4
        
        total_num = 0   
        cv2.imshow("Video", frame)
        
        
    key = cv2.waitKey(33)  # 1) & 0xFF

    if key == 27:  # esc 종료
        break

cap.release()
# if not cv2.destroyAllWindows():
#     import stream    






