# 2021_CapstoneDesign_ParkinglotSystem
Parking space tracking system with Deep Learning
2021년 1학기 캡스톤디자인 과제

## 구성원

### 이헌욱 (20163075)

[git 주소](https://github.com/HeonUk-Lee)

### 이현학 (20163076)

[git 주소](https://github.com/hh0260)

## 실행 환경

- Language : Python
- Python version "3.8.5" 
- Window 10 64bit

## 실행 방법

- get_line.py 파일을 통해 주차영상에서 주차선을 설정합니다.
- output.py 파일을 통해 주차공간을 실시간으로 추적합니다.
- stream.py 파일을 통해 결과영상을 스트리밍합니다.

## 프로그램 구성 요소

### get_line.py

실시간 주차영상을 받아와서 주차선을 설정합니다.

OpenCV를 활용하여 받은 사용자의 마우스 입력을 통해 주차선의 좌표를 텍스트 파일로 저장합니다.
![line](https://user-images.githubusercontent.com/74241873/110746580-5a756580-8280-11eb-9b4a-16bea89b6b1b.jpg)


### output.py

get_line.py에서 생성된 좌표와 미리학습된 모델을 활용하여 해당 좌표 내 공간이 주자가능 영역인지 아닌지를 판단합니다.

주차가능한 구역은 초록색, 불가능한 구역은 빨간색으로 표시합니다. 
![image](https://user-images.githubusercontent.com/74241873/110746807-b3dd9480-8280-11eb-82a3-aaef5fdda1b2.png)


### stream.py
실시간 처리된 영상을 다시 웹스트리밍합니다.
