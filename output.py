# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:26:25 2021

@author: hh026
"""
import cv2
import tensorflow as tf
from space_classification import Space_classification
from PyQt5 import QtWidgets


class Output:
    
    def show_video(MainWindow, videosource, video_scale, cal_cycle):        
        
        error_code = Space_classification.checkfile()
        
        if error_code == 0:   #학습모델
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no trained model file.") 
            return
        if error_code == 1:   #좌표파일없음
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no point lists file.")  
            return
            
        cap = cv2.VideoCapture(videosource)
        MainWindow.hide()
        if not cap.isOpened():   #url주소
            QtWidgets.QMessageBox.warning(MainWindow, "Load failed", "Failed to load video(Invalid url address)") 
            cap.release()
            MainWindow.show()
            return
        MainWindow.show()
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * video_scale) #3
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * video_scale) #4
        
        point_list = []   
        point_list = Space_classification.list_point()    #좌표 불러오기        
        model = tf.keras.models.load_model('parking_model.h5') #학습모델 불러오기
       
        close_flag = False
        count = 0     

        while (cap.isOpened):
    
            ret, frame = cap.read()
            count += 1
            
            if ret == False:
                QtWidgets.QMessageBox.warning(MainWindow, "Load failed", "Failed to load video") 
                break
            
            frame = cv2.resize(frame, (width, height))
           
            if count == cal_cycle:
                
                frame, result_text = Space_classification.classification(frame, point_list, model)
                cv2.imshow("Video", frame)
                close_flag = True
                count = 0  
                
            if close_flag and cv2.getWindowProperty('Video', 0) < 0:
                break
        
            key = cv2.waitKey(33)  # 1) & 0xFF

            if key == 27:  # esc 종료
                break
            

        cap.release()
        cv2.destroyAllWindows()