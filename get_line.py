import cv2
from PyQt5 import QtWidgets
import Inputnum_ui

class Get_line:
    
    # Mouse Callback함수 : 파라미터는 고정됨.
    def Mouse_Click(event, x, y, flags, param):
        global count, num_input, x0, y0, x1, y1, x2, y2, x3, y3, draw_image, image_list, point_list
    
        if event == cv2.EVENT_LBUTTONDOWN:                      # 마우스를 클릭s
            if count == 0:
                x0, y0 = x, y
            elif count == 1:
                x1, y1 = x, y
                cv2.line(draw_image,(x0,y0),(x1, y1),(255,0,0),2)            
            elif count == 2:
                x2, y2 = x, y
                cv2.line(draw_image,(x1,y1),(x2, y2),(255,0,0),2)            
            elif count == 3:            
                x3, y3 = x, y
                cv2.line(draw_image,(x2,y2),(x3, y3),(255,0,0),2)            
                cv2.line(draw_image,(x0,y0),(x3, y3),(255,0,0),2) 
                cv2.imshow("image", draw_image)
                count += 1
                while True:
                    Dialog = QtWidgets.QDialog()
                    ui = Inputnum_ui.Ui_Inputnum()
                    ui.setupUi(Dialog)
                    Dialog.show()                    
                    if not Dialog.exec_():   # cancel 누르는 경우  
                        draw_image = image_list[-1].copy()
                        cv2.imshow("image", draw_image)
                        count = -1
                        break
                    elif Inputnum_ui.space_num.isdigit():   # 숫자 입력한 경우  
                        if int(Inputnum_ui.space_num) < 1 or int(Inputnum_ui.space_num) > 20:
                            QtWidgets.QMessageBox.information(Dialog, "Input Warning", "Please enter only numbers in the range 1 to 20.")
                            continue
                        num_input = True  
                        break
                    else:  #다른 문자 입력한 경우
                        QtWidgets.QMessageBox.information(Dialog, "Input Warning", "Please enter only numbers in the range 1 to 20.")
                        continue

            count += 1   

    def addlines(image):
        global count, num_input, x0, y0, x1, y1, x2, y2, x3, y3, draw_image, image_list, point_list
        
        count = 0
        num_input = False
        x0 = y0 = x1 = y1 = -1
        x2 = y2 = x3 = y3 = -1
        
        image_list = []  #이미지 스택
        space_num_list = []
        point_list = []
        
        draw_image = image.copy()
        image_list.append(draw_image.copy()) #원본 저장
        space_num_list.append(0)
        
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',Get_line.Mouse_Click)  # 마우스 이벤트 후 callback 수행하는 함수 지정

        while True:
            cv2.imshow("image", draw_image)    # 화면을 보여준다.

            k = cv2.waitKey(10) & 0xFF   # 키보드 입력값을 받고
            
            if k == 27:     # esc를 누르면 종료
                break
    
            if k == 115:    #S = 저장하기: 이미지, 좌표
                list_pt = list(map(str, point_list))
                
                with open('points.txt', 'w') as f:    # 파일을 쓰기 모드(w)로 열기
                    for line in list_pt:
                        f.write(line+'\n')
                cv2.imwrite("./line.jpg", draw_image)   
                cv2.waitKey(1000)   #1초 뒤 종료
                break    
            
            if k == 26 and len(image_list) > 1:  # ctrl + z : 한 단계 되돌리기
                image_list.pop()
                draw_image = image_list[-1].copy()
                del(point_list[-4*(space_num_list.pop()):])
                cv2.imshow("image", draw_image)
                count = 0
                
        
            if num_input == True:    #숫자 입력하고 그리기
                side_01 = (x0-x1)**2 + (y0-y1)**2
                side_03 = (x0-x3)**2 + (y0-y3)**2
                if  side_01 < side_03:  #***여기 조건은 개선필요(숫자 2입력시 가로세로)***
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
                i=0
            
                while i < len(point_list)-3:
                    cv2.line(draw_image,point_list[i],point_list[i+1],(255,0,0),2)
                    cv2.line(draw_image,point_list[i+1],point_list[i+2],(255,0,0),2)
                    cv2.line(draw_image,point_list[i+2],point_list[i+3],(255,0,0),2)
                    cv2.line(draw_image,point_list[i+3],point_list[i],(255,0,0),2)
                    i += 4
                    
                image_list.append(draw_image.copy())
                space_num_list.append(space_num)
                num_input = False
                count = 0

            if cv2.getWindowProperty('image', 0) < 0:
                break

        cv2.destroyAllWindows()
    
    def capture(videosource):
        cap = cv2.VideoCapture(videosource)
        iscapture = False
        closecount = 0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))//2 #3
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))//2 #4
        while (cap.isOpened):            
            ret, frame = cap.read()
            if ret == False:
                break
            frame = cv2.resize(frame, (width, height))
        
            key = cv2.waitKey(33)  # 1) & 0xFF
            if not iscapture:
                if closecount > 0 and cv2.getWindowProperty('Video', 0) < 0: #동영상 닫기
                    break
                cv2.imshow("Video", frame)
                closecount += 1
            if key == 27:  # esc 종료
                break
            elif key == 26:  # ctrl + z
                iscapture = True
                cv2.imwrite("./cap.jpg", frame)   
                img = cv2.imread("./cap.jpg"); #이미지 불러오기
                cv2.imshow("Video",img);
            if cv2.getWindowProperty('Video', 0) < 0:   #캡쳐 이후 닫기
                break

                
        cap.release()
        cv2.destroyWindow("Video")

#개선사항0. 원근감 반영하기
#개선사항1. 2칸 입력시 가로세로 조건
#개선사항2. 사각형 그리는 순서 고지
#개선사항3. 기능들 표시


