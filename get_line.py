import cv2
import os

cwd = os.getcwd() #작업 중인 디렉토리

print(cwd)
print(type(cwd))


#""" 비디오에서 캡처
cap = cv2.VideoCapture("./video.h264")
#cap = cv2.VideoCapture("http://keycalendar.iptime.org:8091/?action=stream")

#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #3
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #4

while (cap.isOpened):
    
    ret, frame = cap.read()
    if ret == False:
        break

    cv2.imshow("VideoFrame", frame)

    #now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    key = cv2.waitKey(33)  # 1) & 0xFF

    if key == 27:  # esc 종료
        break
    elif key == 26:  # ctrl + z
        #cv2.IMREAD_UNCHANGED
        cv2.imwrite("./cap.jpg", frame)   
        img = cv2.imread("./cap.jpg"); #이미지 불러오기
        cv2.imshow("image",img);

cap.release()
cv2.destroyAllWindows()
#"""



'''OpenCV 차선검출 함수(보류)
def select_rgb_white_yellow(image): #2.흰색, 노란색 분리
    # white color mask
    lower = np.uint8([120, 120, 120])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    # yellow color mask
    yellow_lower = np.uint8([0, 170, 170])
    yellow_upper = np.uint8([255, 255, 255])
    yellow_mask = cv2.inRange(image, yellow_lower, yellow_upper)
    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    masked = cv2.bitwise_and(image, image, mask = mask)
    return masked

def convert_gray_scale(image): #3.gray로 변환
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size): #4.가우시안 블러
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def detect_edges(image, low_threshold=50, high_threshold=200): #5.캐니엣지 검출
    return cv2.Canny(image, low_threshold, high_threshold)

def filter_region(image, vertices):
    """
    Create the mask using the vertices and apply it to the input image
    """
    mask = np.zeros_like(image)
    if len(mask.shape)==2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension        
    return cv2.bitwise_and(image, mask)
    
def select_region(image): #6.관심영역 지정
    """
    It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    """
    # first, define the polygon by vertices
    rows, cols = image.shape[:2]
    pt_1  = [cols*0.527, rows*0.319]
    pt_2 = [cols*0.37, rows*0.738]
    pt_3 = [cols*0.74, rows*0.997]
    pt_4 = [cols*0.86, rows*0.50]
    # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
    vertices = np.array([[pt_1, pt_2, pt_3, pt_4]], dtype=np.int32)
    return filter_region(image, vertices)

def draw_lines(img, lines, color=[0, 0, 255], thickness=3): # 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): #7.허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)

    return line_img

def weighted_img(img, initial_img, α=1, β=1., λ=0.): #8.두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, α, img, β, λ)


white_yellow_image = select_rgb_white_yellow(image)
gray_image = convert_gray_scale(white_yellow_image)
blur_image = gaussian_blur(gray_image, 5)
edge_image = detect_edges(blur_image)

####여기에서 사용자 입력 받기####

roi_image = select_region(edge_image)
hough_image = hough_lines(roi_image, 0.8, 1 * np.pi/180, 90, 10, 100) # 허프 변환
result = weighted_img(hough_image, image) # 원본 이미지에 검출된 선 overlap

cv2.imshow("SOURCE", image)
#cv2.imshow("white_yellow", white_yellow_33image )
#cv2.imshow("gray", gray_image )
#cv2.imshow("blur", blur_image )
#cv2.imshow("edge", edge_image )
#cv2.imshow("roi", roi_image )
cv2.imshow("hough", hough_image )
cv2.imshow("result", result)

'''


#'''사용자입력 차선 검출
#image = cv2.imread("./cap01.jpg", cv2.IMREAD_COLOR); #1.BGR이미지 불러오기
#image = cv2.imread("./cap02.jpg", cv2.IMREAD_COLOR); #1.BGR이미지 불러오기
image = cv2.imread("./cap.jpg", cv2.IMREAD_COLOR); #1.BGR이미지 불러오기

#cv2.waitKey(0)
#cv2.destroyAllWindows()

draw_image = image.copy()

count = 0
num_input = False
x0, y0 = -1, -1
x1, y1 = -1, -1
x2, y2 = -1, -1
x3, y3 = -1, -1
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

cv2.namedWindow('image')
cv2.setMouseCallback('image',Mouse_Click)  # 마우스 이벤트 후 callback 수행하는 함수 지정

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

cv2.destroyAllWindows()

#개선사항0. 원근감 반영하기
#개선사항1. 2칸 입력시 가로세로 조건
#개선사항2. 사각형 그리는 순서 고지
#개선사항3. 기능들 표시


