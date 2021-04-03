# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\drawline.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import cv2
import os
from PyQt5 import QtCore, QtWidgets
from get_line import Get_line


class Ui_Drawline(object):
    
    def __init__(self, videosource):
        self.videosource = videosource
        super().__init__()
    
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Draw line")
        self.Dialog.resize(413, 293)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton = QtWidgets.QPushButton(self.Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 80, 141, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 150, 141, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonBox_2 = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_2.setGeometry(QtCore.QRect(310, 10, 81, 32))
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Help)
        self.buttonBox_2.setObjectName("buttonBox_2")

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

        self.buttonBox_2.clicked.connect(self.help_clicked)
        self.pushButton.clicked.connect(self.capture_clicked)
        self.pushButton_2.clicked.connect(self.addlines_clicked)

    def help_clicked(self):
        QtWidgets.QMessageBox.information(self.Dialog, "help", "Capture: 주차장 선그리기를 위한 이미지 추출\n"
                                                               "\tCtal+z: 캡쳐\n\tEsc: 종료\n"
                                                               "\nAdd lines: 주차장 선그리기\n"
                                                               "\n마우스 좌클릭: 주차선 그리기\n\tS: 저장\n\tCtal+z: 되돌리기\n\tEsc: 종료")

    def capture_clicked(self):     
        self.button_set(False)
        cap = cv2.VideoCapture(self.videosource)
        if not cap.isOpened():   #url주소
            QtWidgets.QMessageBox.warning(self.Dialog, "Load failed", "Failed to load video(Invalid url address)") 
        else:
            Get_line.capture(cap)
        cap.release()
        self.button_set(True) 

    def addlines_clicked(self):  
        if not os.path.isfile('./cap.jpg'):
            return
        image = cv2.imread("./cap.jpg", cv2.IMREAD_COLOR);        
        self.button_set(False)        
        Get_line.addlines(image)        
        self.button_set(True)        
    
    def button_set(self, flag):
        self.pushButton.setEnabled(flag)
        self.pushButton_2.setEnabled(flag)
        self.buttonBox.setEnabled((flag))
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Draw line"))
        self.pushButton.setText(_translate("Dialog", "Capture"))
        self.pushButton_2.setText(_translate("Dialog", "Add lines"))

    