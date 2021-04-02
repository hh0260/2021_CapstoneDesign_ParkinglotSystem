# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:26:25 2021

@author: hh026
"""
import cv2
import os
import numpy as np
import tensorflow as tf
from makevideo import MakeVideo


class Output:
    
    def checkfile():
        if not os.path.isfile('parking_model.h5'):
            return 0     
        if not os.path.isfile('points.txt'):
            return 1 
    
    def show_video(videosource):
        cap = cv2.VideoCapture(videosource)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))//2 #3
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))//2 #4
        

        
        point_list = []   
        point_list = MakeVideo.list_point()    #좌표 불러오기        
        model = tf.keras.models.load_model('parking_model.h5') #학습모델 불러오기
       
        #class_names = ['car','empty']
        count = 0     
        #total_num = 0 

        while (cap.isOpened):
    
            ret, frame = cap.read()
            count += 1
            if ret == False:
                break
            frame = cv2.resize(frame, (width, height))
            if count == 5:
                count = 0
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
                    #print(str(total_num)+": "+class_names[np.argmax(score)]+", "+str(100 * np.max(score)))
                    #total_num += 1
                    if np.argmax(score):
                        frame = MakeVideo.draw_poly(frame, point_list, i, [0, 255, 0])
                
                    i += 4        
                #total_num = 0   
                cv2.imshow("Video", frame)
        
        
            key = cv2.waitKey(33)  # 1) & 0xFF

            if key == 27:  # esc 종료
                break

        cap.release()
        cv2.destroyAllWindows()
 


    

    






