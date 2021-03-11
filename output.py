# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:26:25 2021

@author: hh026
"""
import cv2
import numpy as np
import tensorflow as tf


#cwd = os.getcwd() #작업 중인 디렉토리

cap = cv2.VideoCapture("./video.h264")
#cap = cv2.VideoCapture("http://keycalendar.iptime.org:8091/?action=stream")

#좌표 텍스트 파일 읽어오기

with open('points.txt', 'r') as text_file:
    point_list = []
    
    while True:
        line = text_file.readline().strip('\n')    
        if line == '':
            break
        ptline = line.strip("( )")
        ptline = ptline.split(", ")
        ptline = list(map(int, ptline))  #숫자로 변환 
        ptline = tuple(ptline)
        point_list.append(ptline)

    

#저장된 모델 불러오기
model = tf.keras.models.load_model('parking_model.h5')

#이미지 변환 100x200
def warp_image(image, xy0, xy1, xy2, xy3, height = 100, width = 200):
    pt1 = np.float32([[xy0[0],xy0[1]],[xy1[0],xy1[1]],[xy2[0],xy2[1]],[xy3[0],xy3[1]]])
    pt2 = np.float32([[0,0],[0,height],[width,height],[width,0]])
    
    M = cv2.getPerspectiveTransform(pt1,pt2)
    img_result = cv2.warpPerspective(image, M, (width,height))
    
    return img_result



def draw_poly(image, point_list, i, color=[0, 0, 255]):
    
    cv2.line(image,point_list[i], point_list[i+1],color,2)
    cv2.line(image,point_list[i+1], point_list[i+2],color,2)
    cv2.line(image,point_list[i+2], point_list[i+3],color,2)
    cv2.line(image,point_list[i+3], point_list[i],color,2)




class_names = ['car','empty']
count = 0     
spot_num = 0   
total_num = 0 

while (cap.isOpened):
    
    ret, frame = cap.read()
    count += 1
    if ret == False:
        break
    if count == 10:
        count = 0
        image = np.copy(frame)   
        
        i=0
        while i < len(point_list)-3:   #모든 영역 빨간색
            draw_poly(image, point_list, i, [0, 0, 255])
            i += 4      
        
        i=0
        while i < len(point_list)-3:
            img = warp_image(frame, point_list[i], point_list[i+1], 
                             point_list[i+2], point_list[i+3])
            
            img = tf.expand_dims(img, 0)
            predictions = model.predict(img)
            score = tf.nn.softmax(predictions[0])
            
            print(str(total_num)+": "+class_names[np.argmax(score)]+", "+str(100 * np.max(score)))
            total_num += 1
            if np.argmax(score):
                draw_poly(image, point_list, i, [0, 255, 0])
                
            i += 4
        print("------------------")
        total_num = 0   
        cv2.imshow("Video", image)
        #cv2.imshow("ROI", img)   
        
        
    key = cv2.waitKey(33)  # 1) & 0xFF

    if key == 27:  # esc 종료
        break

cap.release()
cv2.destroyAllWindows()






