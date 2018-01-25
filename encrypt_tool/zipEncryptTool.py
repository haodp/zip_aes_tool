# -*- coding: utf-8 -*-
import sys
import os,os.path
import aeszip
import Log

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtPrintSupport, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

class zipEncryptTool(QtWidgets.QWidget):
    def __init__(self):
        super(zipEncryptTool, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(150, 150, 800, 450)
        self.setWindowTitle('zip aes tool')

        self.label = QtWidgets.QLabel("path:", self)
        self.label.setGeometry(QtCore.QRect(50, 100, 50, 30))

        # combo.activated.connect(self.onActivated)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(100, 100, 400, 30))
        self.textEdit.setObjectName("textEdit")

        browseButton = QtWidgets.QPushButton(self)
        browseButton.setText("选择文件夹")
        browseButton.setGeometry(QtCore.QRect(510, 100, 90, 30))
        browseButton.setObjectName("browseButton")
        browseButton.clicked.connect(self.browseForlderEvent)

        fileBrowseButton = QtWidgets.QPushButton(self)
        fileBrowseButton.setText("选择文件")
        fileBrowseButton.setGeometry(QtCore.QRect(610, 100, 80, 30))
        fileBrowseButton.setObjectName("fileBrowseButton")
        fileBrowseButton.clicked.connect(self.browseFileEvent)

        encryptButton = QtWidgets.QPushButton(self)
        encryptButton.setText("加密")
        encryptButton.setGeometry(QtCore.QRect(120, 150, 60, 35))
        encryptButton.setObjectName("encryptButton")
        encryptButton.clicked.connect(self.encryptEvent)

        dencryptButton = QtWidgets.QPushButton(self)
        dencryptButton.setText("解密")
        dencryptButton.setGeometry(QtCore.QRect(200, 150, 60, 35))
        dencryptButton.setObjectName("dencryptButton")
        dencryptButton.clicked.connect(self.dencryptEvent)

    #解密
    def dencryptEvent(self, *args, **kwargs):
        filePath = self.textEdit.toPlainText()

        if not filePath.endswith(".zip"):
            reply = QMessageBox.critical(self,"Error",self.tr("解密对象必须为zip文件。"))
            if reply == QMessageBox.Ok:
                return

        if not os.path.exists(filePath):
            reply = QMessageBox.critical(self,"Error",self.tr("解密对象不存在。"))
            if reply == QMessageBox.Ok:
                return

        # 解密路径
        targetPath = filePath[0:len(filePath) - 4]
        result = aeszip.zip_dencrypt(filePath, targetPath)
        result_reply = None
        if result:
            result_reply = QMessageBox.information(self, "结果", "解密成功。<br/>路径:" + targetPath,QMessageBox.Ok)
        else:
            result_reply = QMessageBox.information(self, "结果", "解密失败。", QMessageBox.Ok)

        if result_reply == QMessageBox.Ok:
            return


    # 加密
    def encryptEvent(self, *args, **kwargs):
        filePath = self.textEdit.toPlainText()

        if not os.path.exists(filePath):
            reply = QMessageBox.critical(self,"Error",self.tr("加密对象不存在。"))
            if reply == QMessageBox.Ok:
                return

        if filePath.endswith(".zip"):
            reply = QMessageBox.warning(self, 'Warn', '你确定要对zip文件再加密?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print("对zip文件再加密处理.")
            else:
                return

        targetPath = ""
        if os.path.isfile(filePath): #文件
            if filePath.endswith(".zip"):
                targetPath = filePath[0:len(targetPath) - 4] + "2.zip"
            elif filePath.find(".") > 0:
                filelist = filePath.split(".")
                filetype = filelist[len(filelist) - 1]
                length = len(filePath) - len(filetype) - 1
                targetPath = filePath[0:length] + ".zip"
            else:
                targetPath = filePath + ".zip"
        else:
            if filePath.endswith(os.path.altsep):
                targetPath = filePath[0:len(filePath) - 1] + ".zip"
            else:
                targetPath = filePath + ".zip"

        result = aeszip.zip_encrypt(filePath, targetPath)
        result_reply = None
        if result:
            result_reply = QMessageBox.information(self, "结果", "加密成功。<br/>路径:" + targetPath,QMessageBox.Ok)
        else:
            result_reply = QMessageBox.information(self, "结果", "加密失败。", QMessageBox.Ok)

        if result_reply == QMessageBox.Ok:
            return

    def browseForlderEvent(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "/")  # 起始路径
        # print(directory1)
        self.textEdit.setText(directory)

    def browseFileEvent(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "/", # 起始路径
                                                          "All Files (*);;Text Files (*.zip)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.textEdit.setText(fileName)

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication([])
        ex = zipEncryptTool()
        ex.show()
        sys.exit(app.exec_())
    except QtWidgets.QErrorMessage as e:
        Log.logger.error(e.showMessage())
        print (e.showMessage())
    except Exception as ex:
        Log.logger.error(ex.showMessage())
        print (ex.showMessage())
