import cv2
import os

class MakeLine:
    count = 0
    num_input = False
    x0, y0 = -1, -1
    x1, y1 = -1, -1
    x2, y2 = -1, -1
    x3, y3 = -1, -1
    # 비디오에서 캡처
    def capture(camera):
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))//2 #3
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))//2 #4
        while (camera.isOpened):
            
            ret, frame = camera.read()
            if ret == False:
                break
            frame = cv2.resize(frame, (width, height))
            cv2.imshow("Video", frame)
            
            key = cv2.waitKey(33)  # 1) & 0xFF
            if key == 27:  # esc 종료
                cv2.destroyWindow("Video")
                cv2.destroyWindow("image")
                break
            elif key == 26:  # ctrl + z
                cv2.imwrite("./cap.jpg", frame)   
                img = cv2.imread("./cap.jpg"); #이미지 불러오기
                cv2.imshow("image",img);
                  
    # Mouse Callback함수 : 파라미터는 고정됨.
    def Mouse_Click(event, x, y, flags, param):
        global count, num_input, x0, y0, x1, y1, x2, y2, x3, y3
    
        if event == cv2.EVENT_LBUTTONDOWN:                      # 마우스를 클릭
            print("(" + str(x) + ", " + str(y) + ")")
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
            elif count > 3 and num_input == True:
                num_input = False
            count += 1   
            
    #사용자입력 차선 검출            
    def draw(camera):
        global count, num_input, x0, y0, x1, y1, x2, y2, x3, y3
        image = cv2.imread("./cap.jpg"); #이미지 불러오기
        draw_image = image.copy()
        
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',MakeLine.Mouse_Click)  # 마우스 이벤트 후 callback 수행하는 함수 지정
        point_list = []
        
        while True:
            cv2.imshow("image", draw_image)    # 화면을 보여준다.

            k = cv2.waitKey(10) & 0xFF   # 키보드 입력값을 받고
            #print(k)
            if k == 27:     # esc를 누르면 종료
                break
            if k == 32:    #스페이스 바 = 다시 그리기
                count = 0
                draw_image = image.copy()
                point_list = []
            
            if k == 115:    #S = 저장하기: 이미지, 좌표
                list_pt = list(map(str, point_list))
                
                with open('points.txt', 'w') as f:    # 파일을 쓰기 모드(w)로 열기
                    for line in list_pt:
                        f.write(line+'\n')
                cv2.imwrite("./line.jpg", draw_image)   
                cv2.waitKey(800)   #0.8초 뒤 종료
                break
            
                    
            if 48 < k < 58 and count > 3:    #숫자 입력하면 그리기
                side_01 = (x0-x1)**2 + (y0-y1)**2
                side_03 = (x0-x3)**2 + (y0-y3)**2
                slot_num = k - 48
                if  side_01 < side_03:  #여기 조건은 개선필요(숫자 2입력시 가로세로) 
                    x0, x1, x2, x3 = x1, x2, x3, x0
                    y0, y1, y2, y3 = y1, y2, y3, y0
                gap_x01 = (int)((x1-x0)/(slot_num))
                gap_y01 = (int)((y1-y0)/(slot_num))
                gap_x32 = (int)((x2-x3)/(slot_num))
                gap_y32 = (int)((y2-y3)/(slot_num))
                
                i=0
                for i in range(slot_num):  #각 사각형 별 좌표 구하기
                    #점0
                    point_list.append((x0 + i*gap_x01, y0 + i*gap_y01))
                    #점1
                    point_list.append((x0 + (i+1)*gap_x01, y0 + (i+1)*gap_y01))
                    #점2
                    point_list.append((x3 + (i+1)*gap_x32, y3 + (i+1)*gap_y32))
                    #점3
                    point_list.append((x3 + i*gap_x32, y3 + i*gap_y32))
                    
                    print(point_list)
        
                    
                #사각형 그리기
                draw_image = image.copy()
                i=0
                    
                while i < len(point_list)-3:
                    cv2.line(draw_image,point_list[i],point_list[i+1],(255,0,0),2)
                    cv2.line(draw_image,point_list[i+1],point_list[i+2],(255,0,0),2)
                    cv2.line(draw_image,point_list[i+2],point_list[i+3],(255,0,0),2)
                    cv2.line(draw_image,point_list[i+3],point_list[i],(255,0,0),2)
                    i += 4
                        
                num_input = True   #숫자입력 완료
                count = 0      
    
    
# cap.release()
# cv2.destroyAllWindows()

#개선사항0. 원근감 반영하기
#개선사항1. 2칸 입력시 가로세로 조건
#개선사항2. 사각형 그리는 순서 고지
#개선사항3. 기능들 표시

