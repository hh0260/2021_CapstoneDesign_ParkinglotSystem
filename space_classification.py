# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 02:42:20 2021

@author: hh026
"""

import cv2
import os
import numpy as np
import tensorflow as tf

cl = ['car', 'empty']
 
class Space_classification:
    
    def checkfile():
        if not os.path.isfile('parking_model.h5'):
            return 0     
        if not os.path.isfile('points.txt'):
            return 1 
 
    def list_point():
        point_list = []
        with open('points.txt', 'r') as text_file:
    
            while True:
                line = text_file.readline().strip('\n')    
                if line == '':
                    break
                ptline = line.strip("( )")
                ptline = ptline.split(", ")
                ptline = list(map(int, ptline))  #숫자로 변환 
                ptline = tuple(ptline)
                point_list.append(ptline)
                
        return point_list
     
    #이미지 변환 64x128
    def warp_image(image, xy0, xy1, xy2, xy3, height = 64, width = 128):
        #x_list = [xy0[0],xy1[0],xy2[0],xy3[0]]
        #y_list = [xy0[1],xy1[1],xy2[1],xy3[1]]
        #pt1 = np.float32([[min(x_list),min(y_list)],[min(x_list),max(y_list)],[max(x_list),max(y_list)],[max(x_list),min(y_list)]])
        
        if abs(xy3[0]-xy0[0])>abs(xy3[1]-xy0[1]):
            pt1 = np.float32([[xy0[0],xy0[1]],[(xy0[0]+xy1[0])/2,(xy0[1]+xy1[1])/2],[(xy2[0]+xy3[0])/2,(xy2[1]+xy3[1])/2],[xy3[0],xy3[1]]])    
            #print("가로")
        else:
            pt1 = np.float32([[xy0[0],xy0[1]],[xy1[0],xy1[1]],[xy2[0],xy2[1]],[xy3[0],xy3[1]]])    
            #print('세로')
        pt2 = np.float32([[0,0],[0,height],[width,height],[width,0]])
        
        M = cv2.getPerspectiveTransform(pt1,pt2)
        img_result = cv2.warpPerspective(image, M, (width,height))
        #cv2.imshow("Video1", img_result)
        #cv2.imwrite("./555.jpg",img_result)
        
        return img_result
    

    def draw_poly(image, point_list, i, color=[0, 0, 255], thic = 2):
        
        cv2.line(image,point_list[i], point_list[i+1],color, thic)
        cv2.line(image,point_list[i+1], point_list[i+2],color, thic)
        cv2.line(image,point_list[i+2], point_list[i+3],color, thic)
        cv2.line(image,point_list[i+3], point_list[i],color, thic)
        
        return image
    
    
    def classification(frame, point_list, model):        
        
        cut = np.copy(frame)
        #흑백처리
        cut = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
        
        #블러처리
        cut = cv2.blur(cut, (5,5), 0)
        #cv2.imwrite("./blur.jpg",cut)        
        
        #히스토그램 CLAHE 평탄화
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5,5))
        cut = clahe.apply(cut)
        #cv2.imwrite("./result.jpg",cut)
        
        
        cut = cv2.cvtColor(cut, cv2.COLOR_GRAY2BGR)
        total_num = 0
        freespot_num = 0
        
        #array5 = np.full(cut.shape, (20, 20, 20), dtype=np.uint8)
        #cut = cv2.add(cut, array5)
        
        
        i=0
        while i < len(point_list)-3:   #모든 영역 빨간색
            frame = Space_classification.draw_poly(frame, point_list, i, [0, 0, 255])
            i += 4      
            
        i=0
        while i < len(point_list)-3:
            img = Space_classification.warp_image(cut, point_list[i], point_list[i+1], 
                                                  point_list[i+2], point_list[i+3])
            
            img_clsf = tf.expand_dims(img, 0)
            
            
            predictions = model.predict(img_clsf)
            score = tf.nn.softmax(predictions[0])            
            #print(str(total_num)+": "+str(cl[np.argmax(score)])+", "+str(100 * np.max(score)))  #분류결과 확인
            total_num += 1
            if np.argmax(score):
                freespot_num += 1
                frame = Space_classification.draw_poly(frame, point_list, i, [0, 255, 0], 4)
                # cv2.imwrite("C:/Users/hh0260/Desktop/PKLot/empty/"+str(point_list[i])+str(int(i/4))+'.jpg',img)
            # else:
                # cv2.imwrite("C:/Users/hh0260/Desktop/PKLot/car/"+str(point_list[i])+str(int(i/4))+'.jpg',img)
            i += 4        
                    
                    
        result_text = str(freespot_num)  + "/"+ str(total_num)
        cv2.putText(frame, result_text, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 6, cv2.LINE_AA)
        
        return frame, result_text
        
        
        

