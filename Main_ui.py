# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtWidgets
from set_line import Set_line  
from output import Output 


videosource = "./video.h264"
#videosource = "http://keycalendar.iptime.org:8091/?action=stream"
#videosource = "http://wrong.address"
park_name = "55호관"
video_scale = 0.5
video_frame = 3

class Ui_MainWindow(object):    
 
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(466, 318)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(370, 10, 81, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Help)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 50, 151, 221))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 260, 271, 31))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        MainWindow.setWindowTitle("main")
        self.pushButton.setText("Set line")
        self.pushButton_2.setText("Check output")
        self.pushButton_3.setText("Stream")        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.buttonBox.clicked.connect(self.help_clicked)
        self.pushButton.clicked.connect(self.setline_clicked)
        self.pushButton_2.clicked.connect(self.checkoutput_clicked)
        self.pushButton_3.clicked.connect(self.stream_clicked)

    def help_clicked(self):
        QtWidgets.QMessageBox.about(MainWindow, "help", "Set line - 주차선 가이드 설정\n"
                                                        "           * 주차선 입력: 마우스 클릭\n"
                                                        "           * 되돌리기: Ctrl+z\n"
                                                        "           * 저장: S\n"
                                                        "           * 종료: Esc\n"
                                                        "\nCheck output - 결과 영상 확인\n"
                                                        "\nStream - 결과 영상 스트리밍 시작")

    def setline_clicked(self):    
        self.button_set(False)        
        Set_line.addlines(MainWindow, videosource, video_scale)        
        self.button_set(True) 
        
    def checkoutput_clicked(self):
        self.button_set(False)
        Output.show_video(MainWindow, videosource, video_scale, video_frame)
        self.button_set(True) 
        
    def stream_clicked(self):   
        from stream import Stream   
        self.button_set(False)
        MainWindow.hide()
        Stream.init_stream(MainWindow, videosource, video_scale, video_frame, park_name)  
        self.button_set(True)
        MainWindow.show()
        
    def button_set(self, flag):
        self.pushButton.setEnabled(flag)
        self.pushButton_2.setEnabled(flag)
        self.pushButton_3.setEnabled(flag)

    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    

