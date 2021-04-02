# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\drawline.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import cv2
from PyQt5 import QtCore, QtWidgets
from get_line import Get_line


class Ui_Drawline(object):
    
    def __init__(self, videosource):
        self.videosource = videosource
        self.cap = cv2.VideoCapture(videosource)
        super().__init__()
    
    def setup(self, Dialog):
        Dialog.setObjectName("Draw line")
        Dialog.resize(413, 293)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 80, 141, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 150, 141, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonBox_2 = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_2.setGeometry(QtCore.QRect(310, 10, 81, 32))
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Help)
        self.buttonBox_2.setObjectName("buttonBox_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.pushButton.clicked.connect(self.capture_clicked)
        self.pushButton_2.clicked.connect(self.addlines_clicked)

    def capture_clicked(self):
        self.button_set(False)
        Get_line.capture(self.cap)
        self.button_set(True)       

    def addlines_clicked(self):        
        image = cv2.imread("./cap.jpg", cv2.IMREAD_COLOR);        
        self.button_set(False)        
        Get_line.addlines(image)        
        self.button_set(True)        
    
    def button_set(self, flag):
        self.pushButton.setEnabled(flag)
        self.pushButton_2.setEnabled(flag)
        self.buttonBox.setEnabled((flag))
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Draw line"))
        self.pushButton.setText(_translate("Dialog", "Capture"))
        self.pushButton_2.setText(_translate("Dialog", "Add lines"))

    