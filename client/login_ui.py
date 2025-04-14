# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 567)
        Dialog.setSizeIncrement(QSize(0, 0))
        Dialog.setStyleSheet(u"QWidget {\n"
"    background-color: white;\n"
"}\n"
"\n"
"")
        self.LoginForm = QLabel(Dialog)
        self.LoginForm.setObjectName(u"LoginForm")
        self.LoginForm.setGeometry(QRect(150, 10, 171, 71))
        self.LoginForm.setStyleSheet(u"font: 22pt \"Segoe UI\";")
        self.lineEdit_username = QLineEdit(Dialog)
        self.lineEdit_username.setObjectName(u"lineEdit_username")
        self.lineEdit_username.setGeometry(QRect(120, 140, 241, 31))
        self.Password = QLabel(Dialog)
        self.Password.setObjectName(u"Password")
        self.Password.setGeometry(QRect(120, 190, 71, 31))
        self.Password.setStyleSheet(u"QWidget {\n"
"    background-color: pink\n"
";\n"
"}\n"
"font: 18pt \"Segoe UI\";")
        self.lineEdit_password = QLineEdit(Dialog)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setGeometry(QRect(120, 240, 241, 31))
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.pushButton_to_login2 = QPushButton(Dialog)
        self.pushButton_to_login2.setObjectName(u"pushButton_to_login2")
        self.pushButton_to_login2.setGeometry(QRect(130, 350, 231, 24))
        self.Register = QPushButton(Dialog)
        self.Register.setObjectName(u"Register")
        self.Register.setGeometry(QRect(200, 390, 75, 24))
        self.username = QLabel(Dialog)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(120, 100, 61, 21))
        self.username.setStyleSheet(u"QWidget {\n"
"    background-color: pink\n"
";\n"
"}\n"
"font: 18pt \"Segoe UI\";")
        self.pushButton_to_login = QPushButton(Dialog)
        self.pushButton_to_login.setObjectName(u"pushButton_to_login")
        self.pushButton_to_login.setEnabled(True)
        self.pushButton_to_login.setGeometry(QRect(200, 280, 75, 24))
        self.pushButton_to_login.setStyleSheet(u"QWidget {\n"
"    background-color: pink\n"
";\n"
"}\n"
"font: 18pt \"Segoe UI\";")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.LoginForm.setText(QCoreApplication.translate("Dialog", u"      Login", None))
        self.Password.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.pushButton_to_login2.setText(QCoreApplication.translate("Dialog", u"Don\u2019t have an account? ", None))
        self.Register.setText(QCoreApplication.translate("Dialog", u" Register", None))
        self.username.setText(QCoreApplication.translate("Dialog", u"Username", None))
        self.pushButton_to_login.setText(QCoreApplication.translate("Dialog", u"Login", None))
    # retranslateUi
