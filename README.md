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
 #### 본 프로그램은 TensorFlow Keras API를 사용한 이미지 분류 방식으로 실시간 영상의 주차면을 구분함
 #### OpenCV 라이브러리를 사용하여 사전 영상처리 / 결과 영상처리
 #### 애플리케이션을 통해 서버로부터 전송받은 주차정보 및 실시간 영상을 출력

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

- Set line– 클릭 시 주차 가이드 입력화면이 나타난다.
- Check output– 클릭 시 결과 영상을 확인할 수 있다.
- Stream– 클릭 시 결과 영상을 서버로 송출한다.

### set_line.py

주차 가이드 설정: 마우스 입력을 통해 주차면 설정, 's' 키로 저장

![image](https://user-images.githubusercontent.com/74241873/118252481-c758e600-b4e3-11eb-88a1-0fe3aab50964.png)

### Inputnum_ui.py

가이드 설정할 때 숫자 입력하는 UI

### space_classification.py

학습모델 불러와서 이미지분류, 결과 영상 제작

![image](https://user-images.githubusercontent.com/74241873/118252999-5fef6600-b4e4-11eb-8b43-807382e8fdf0.png)
(결과영상)

### output.py

결과영상 출력

### stream.py

결과영상 Flask 웹 스트리밍


## 테스트영상 다운로드
https://drive.google.com/file/d/18kJNkTtR4ZJDcZvqszIgex-rzL48oF8y/view?usp=sharing

#### 프로그램에 대한 자세한 설명은 hh0260@changwon.ac.kr으로 연락바랍니다
