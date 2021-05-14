# 2021_CapstoneDesign_ParkinglotSystem
Deep Learning-based Real-time Parking Management System
2021년 1학기 캡스톤디자인 과제 / 딥 러닝 기반의 실시간 주차 관리 시스템

## 구성원

### 이헌욱 (20163075)

[git 주소](https://github.com/HeonUk-Lee)

### 이현학 (20163076)

[git 주소](https://github.com/hh0260)

## 실행 환경

- Language : Python
- Python version "3.8.5" 
- Window 10 64bit

## 요약
 본 프로그램은 TensorFlow Keras API를 사용한 이미지 분류 방식으로 실시간 영상의 주차면을 구분함
 OpenCV 라이브러리를 사용하여 사전 영상처리 / 결과 영상처리
 애플리케이션을 통해 서버로부터 전송받은 주차정보 및 실시간 영상을 출력

## 실행 방법
### 1. 관리자 프로그램
- video.h264 파일을 다운로드 후 프로그램 폴더에 넣는다.
- Main_ui.py 파일을 실행한다.

### 2. 사용자 모바일 앱
- 사용자 모바일 앱은 관리자가 SelectPark.java내의 'urlAddress'을 관리자 프로그램에서 송출하는 url로 수정 후 사용한다.

## 프로그램 구성 요소

### CNN.py
학습모델 만드는 프로그램, train_data 폴더 내의 이미지셋을 이용하여 CNN 이미지 분류 모델을 학습시키고 해당 모델을 저장한다.

### Main_ui.py

프로그램 메인 UI, 각 기능별로 연결되어있다.

Set line– 클릭 시 주차 가이드 입력화면이 나타난다.
Check output– 클릭 시 결과 영상을 확인할 수 있다.
Stream– 클릭 시 결과 영상을 서버로 송출한다.

![line](https://user-images.githubusercontent.com/74241873/110746580-5a756580-8280-11eb-9b4a-16bea89b6b1b.jpg)


### output.py

get_line.py에서 생성된 좌표와 미리학습된 모델을 활용하여 해당 좌표 내 공간이 주자가능 영역인지 아닌지를 판단합니다.

주차가능한 구역은 초록색, 불가능한 구역은 빨간색으로 표시합니다. 
![image](https://user-images.githubusercontent.com/74241873/110746807-b3dd9480-8280-11eb-82a3-aaef5fdda1b2.png)


### stream.py
실시간 처리된 영상을 다시 웹스트리밍합니다.

## 테스트영상 다운로드
https://drive.google.com/file/d/18kJNkTtR4ZJDcZvqszIgex-rzL48oF8y/view?usp=sharing
