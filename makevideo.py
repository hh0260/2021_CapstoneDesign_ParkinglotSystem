# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 02:42:20 2021

@author: hh026
"""

import cv2
import numpy as np

 
class MakeVideo:
 
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
        
        return image


