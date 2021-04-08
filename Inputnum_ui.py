# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\inputnum.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

space_num = "1"
isEmpty = True

class Ui_Inputnum(object):    
    
    def setupUi(self, Dialog):
        global space_num
        space_num = "1"
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 228)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 60, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 140, 321, 41))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(70, 60, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(2)
        self.lineEdit.textChanged.connect(self.num_change)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName("lineEdit")
        
        Dialog.setWindowTitle("Input number")
        self.label.setText("Enter the number of parking spaces")

        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept) #ok 버튼 따로 처리 
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def num_change(self):  
        global space_num
        space_num=self.lineEdit.text()
