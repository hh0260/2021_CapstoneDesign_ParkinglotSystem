import cv2
from PyQt5 import QtWidgets
import Inputnum_ui

class Set_line:
    
    # Mouse Callback함수 : 파라미터는 고정됨.
    def Mouse_Click(event, x, y, flags, param):        
        
        global count, num_inputflag, x0, y0, x1, y1, x2, y2, x3, y3, frame
        
        if event == cv2.EVENT_LBUTTONDOWN:                      # 마우스를 클릭s
            if count == 0:
                x0, y0 = x, y
                count += 1   
            elif count == 1:
                x1, y1 = x, y
                count += 1             
            elif count == 2:
                x2, y2 = x, y    
                count += 1              
            elif count == 3:      
                x3, y3 = x, y
                count += 1                   
                frame = Set_line.draw_temp(frame, count, x0, y0, x1, y1, x2, y2, x3, y3)           
                cv2.imshow('Set line', frame)
                
                while True:
                    Dialog = QtWidgets.QDialog()
                    ui = Inputnum_ui.Ui_Inputnum()
                    ui.setupUi(Dialog)
                    Dialog.show()                    
                    if not Dialog.exec_():   # cancel 누르는 경우  
                        count = 0
                        break
                    elif Inputnum_ui.space_num.isdigit():   # 숫자 입력한 경우  
                        if int(Inputnum_ui.space_num) < 1 or int(Inputnum_ui.space_num) > 20:
                            QtWidgets.QMessageBox.warning(Dialog, "Input Warning", "Please enter only numbers in the range 1 to 20.")
                            continue
                        num_inputflag = True  
                        break
                    else:  #다른 문자 입력한 경우
                        QtWidgets.QMessageBox.warning(Dialog, "Input Warning", "Please enter only numbers in the range 1 to 20.")
                        continue



    def addlines(MainWindow, videosource, video_scale):
        global count, num_inputflag, x0, y0, x1, y1, x2, y2, x3, y3, point_list, frame
        
        MainWindow.hide()
        
        cap = cv2.VideoCapture(videosource)
        
        if not cap.isOpened():   #url주소
            QtWidgets.QMessageBox.warning(MainWindow, "Load failed", "Failed to load video(Invalid url address)") 
            cap.release()
            MainWindow.show()
            return
        
        MainWindow.show()

        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * video_scale) #3
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * video_scale) #4
        
        count = 0
        close_flag = False
        num_inputflag = False
        x0 = y0 = x1 = y1 = -1
        x2 = y2 = x3 = y3 = -1
        
        space_num_list = []
        point_list = []
        
        cv2.namedWindow('Set line')
        cv2.setMouseCallback('Set line',Set_line.Mouse_Click)  # 마우스 이벤트 후 callback 수행하는 함수 지정

        while True:
            
            ret, frame = cap.read()
            
            if ret == False:
                QtWidgets.QMessageBox.warning(MainWindow, "Load failed", "Failed to load video") 
                break
            
            if close_flag and cv2.getWindowProperty('Set line', 0) < 0: #동영상 닫기
                break
            
            close_flag = True
            frame = cv2.resize(frame, (width, height))
            
            frame = Set_line.draw_list(frame, point_list)       #사각형 그리기   
            frame = Set_line.draw_temp(frame, count, x0, y0, x1, y1, x2, y2, x3, y3)
            cv2.imshow('Set line', frame)
            
            k = cv2.waitKey(33) & 0xFF   # 키보드 입력값을 받고     
            
            if k == 27:     # esc를 누르면 종료
                break
    
            if k == 115:    #S = 저장하기: 이미지, 좌표
                cv2.imwrite("./line.jpg", frame)
                list_pt = list(map(str, point_list))                
                with open('points.txt', 'w') as f:    # 파일을 쓰기 모드(w)로 열기
                    for line in list_pt:
                        f.write(line+'\n')
                cv2.putText(frame, "Saved", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4, cv2.LINE_AA)
                cv2.imshow('Set line', frame)
                cv2.waitKey(1000)   #0.5초 뒤 종료
                break    
            
            if k == 26:  # ctrl + z : 한 단계 되돌리기
                if count > 1: #그리는 도중일때
                    count = 0
                    continue                
                if len(space_num_list) > 0:
                    del(point_list[-4*(space_num_list.pop()):])
                    count = 0
                
        
            if num_inputflag == True:    #숫자 입력하고 그리기
                side_01 = (x0-x1)**2 + (y0-y1)**2
                side_03 = (x0-x3)**2 + (y0-y3)**2
                
                if  side_01 < side_03:
                    x0, x1, x2, x3 = x1, x2, x3, x0
                    y0, y1, y2, y3 = y1, y2, y3, y0
                    
                space_num = int(Inputnum_ui.space_num)
                gap_x01 = (x1-x0)/(space_num)
                gap_y01 = (y1-y0)/(space_num)
                gap_x32 = (x2-x3)/(space_num)
                gap_y32 = (y2-y3)/(space_num)
        
                i=0
                for i in range(space_num):  #각 사각형 별 좌표 구하기
                    #점0
                    point_list.append((int(x0 + i*gap_x01), int(y0 + i*gap_y01)))
                    #점1
                    point_list.append((int(x0 + (i+1)*gap_x01), int(y0 + (i+1)*gap_y01)))
                    #점2
                    point_list.append((int(x3 + (i+1)*gap_x32), int(y3 + (i+1)*gap_y32)))
                    #점3
                    point_list.append((int(x3 + i*gap_x32), int(y3 + i*gap_y32)))
                    
                #사각형 그리기
                frame = Set_line.draw_list(frame, point_list)
                cv2.imshow('Set line', frame)
                space_num_list.append(space_num)
                num_inputflag = False
                count = 0

        cap.release()
        cv2.destroyAllWindows()
    
    def draw_list(frame, point_list):        
        i = 0
        while i < len(point_list)-3:
            cv2.line(frame,point_list[i],point_list[i+1],(255,0,0),2)
            cv2.line(frame,point_list[i+1],point_list[i+2],(255,0,0),2)
            cv2.line(frame,point_list[i+2],point_list[i+3],(255,0,0),2)
            cv2.line(frame,point_list[i+3],point_list[i],(255,0,0),2)
            i += 4
        
        return frame
    
    def draw_temp(frame, count, x0, y0, x1, y1, x2, y2, x3, y3):        

        if count > 1:            
            cv2.line(frame,(x0,y0),(x1, y1),(255,0,0),2)            
        if count > 2:            
            cv2.line(frame,(x1,y1),(x2, y2),(255,0,0),2)            
        if count > 3:      
            cv2.line(frame,(x2,y2),(x3, y3),(255,0,0),2)            
            cv2.line(frame,(x0,y0),(x3, y3),(255,0,0),2) 
        
        return frame

