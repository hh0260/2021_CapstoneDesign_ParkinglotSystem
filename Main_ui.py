# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtWidgets
from Drawline_ui import Ui_Drawline
from output import Output


videosource = "./video.h264"
#videosource = "http://keycalendar.iptime.org:8091/?action=stream"
#videosource = "http://wrong.address"

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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.buttonBox.clicked.connect(self.help_clicked)
        self.pushButton.clicked.connect(self.setline_clicked)
        self.pushButton_2.clicked.connect(self.checkoutput_clicked)
        self.pushButton_3.clicked.connect(self.stream_clicked)

    def help_clicked(self):
        QtWidgets.QMessageBox.information(MainWindow, "help", "Set line:주차장의 주차선 그리기\n"
                                                              "\nCheck output:그려논 주차선 확인\n"
                                                              "\nStream:주차장 스트리밍")

    def setline_clicked(self):
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Drawline(videosource)
        self.ui.setupUi(self.Dialog)
        self.Dialog.show()
        MainWindow.hide()
        self.Dialog.exec_()
        MainWindow.show()
        
    def checkoutput_clicked(self):
        import cv2
        
        self.button_set(False)
        error_code = Output.checkfile()
        cap = cv2.VideoCapture(videosource)
        if not cap.isOpened():   #url주소
            QtWidgets.QMessageBox.warning(MainWindow, "Load failed", "Failed to load video(Invalid url address)") 
        elif  error_code == 0:   #학습모델
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no trained model file.") 
        elif error_code == 1:   #좌표파일없음
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no point lists file.")    
        else:
            Output.show_video(cap)
        cap.release()
        self.button_set(True) 
        
    def stream_clicked(self):   
        import cv2
        from stream import Stream      
        
        self.button_set(False)
        error_code = Output.checkfile()
        cap = cv2.VideoCapture(videosource)
        if not cap.isOpened():   #url주소
            QtWidgets.QMessageBox.warning(MainWindow, "Load failed", "Failed to load video(Invalid url address)") 
        elif  error_code == 0:   #학습모델
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no trained model file.") 
        elif error_code == 1:   #좌표파일없음
            QtWidgets.QMessageBox.warning(MainWindow, "no file", "There is no point lists file.")    
        else:
            MainWindow.hide()
            Stream.init_stream(cap)
            MainWindow.show()
            
        cap.release()
        self.button_set(True)
        
        
    def button_set(self, flag):
        self.pushButton.setEnabled(flag)
        self.pushButton_2.setEnabled(flag)
        self.pushButton_3.setEnabled(flag)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "main"))
        self.pushButton.setText(_translate("MainWindow", "Set line"))
        self.pushButton_2.setText(_translate("MainWindow", "Check output"))
        self.pushButton_3.setText(_translate("MainWindow", "Stream"))
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    

