# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class Ui_RegisterForm(object):
    def setupUi(self, RegisterForm):
        if not RegisterForm.objectName():
            RegisterForm.setObjectName("RegisterForm")
        RegisterForm.resize(531, 581)
        RegisterForm.setMinimumSize(QSize(400, 500))
        self.RegisterForm_1 = QLabel(RegisterForm)
        self.RegisterForm_1.setObjectName("RegisterForm_1")
        self.RegisterForm_1.setGeometry(QRect(230, 10, 201, 61))
        self.RegisterForm_1.setStyleSheet("")
        self.Username = QLabel(RegisterForm)
        self.Username.setObjectName("Username")
        self.Username.setGeometry(QRect(120, 100, 101, 31))
        self.Username.setStyleSheet(
            "QWidget {\n"
            "    background-color: pink\n"
            ";\n"
            "}\n"
            'font: 18pt "Segoe UI";\n'
            ""
        )
        self.Email = QLabel(RegisterForm)
        self.Email.setObjectName("Email")
        self.Email.setGeometry(QRect(120, 180, 111, 31))
        self.Email.setStyleSheet(
            "QWidget {\n"
            "    background-color: pink\n"
            ";\n"
            "}\n"
            'font: 18pt "Segoe UI";\n'
            ""
        )
        self.Password = QLabel(RegisterForm)
        self.Password.setObjectName("Password")
        self.Password.setGeometry(QRect(120, 259, 101, 31))
        self.Password.setStyleSheet(
            "QWidget {\n"
            "    background-color: pink\n"
            ";\n"
            "}\n"
            'font: 18pt "Segoe UI";'
        )
        self.lineEdit_username = QLineEdit(RegisterForm)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_username.setGeometry(QRect(120, 140, 281, 21))
        self.lineEdit_email = QLineEdit(RegisterForm)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.lineEdit_email.setGeometry(QRect(120, 220, 281, 21))
        self.lineEdit_password = QLineEdit(RegisterForm)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setGeometry(QRect(120, 300, 281, 21))
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.pushButton_register = QPushButton(RegisterForm)
        self.pushButton_register.setObjectName("pushButton_register")
        self.pushButton_register.setGeometry(QRect(230, 330, 75, 24))
        self.pushButton_register.setStyleSheet(
            "QWidget {\n"
            "    background-color: pink\n"
            ";\n"
            "}\n"
            'font: 18pt "Segoe UI";'
        )
        self.pushButton_to_login = QPushButton(RegisterForm)
        self.pushButton_to_login.setObjectName("pushButton_to_login")
        self.pushButton_to_login.setGeometry(QRect(180, 440, 171, 24))
        self.pushButton_to_login2 = QPushButton(RegisterForm)
        self.pushButton_to_login2.setObjectName("pushButton_to_login2")
        self.pushButton_to_login2.setGeometry(QRect(210, 480, 101, 24))

        self.retranslateUi(RegisterForm)

        QMetaObject.connectSlotsByName(RegisterForm)

    # setupUi

    def retranslateUi(self, RegisterForm):
        RegisterForm.setWindowTitle(
            QCoreApplication.translate("RegisterForm", "Dialog", None)
        )
        self.RegisterForm_1.setText(
            QCoreApplication.translate(
                "RegisterForm",
                '<html><head/><body><p><span style=" font-size:26pt; vertical-align:sub;">Register</span></p></body></html>',
                None,
            )
        )
        self.Username.setText(
            QCoreApplication.translate("RegisterForm", "     Username", None)
        )
        self.Email.setText(
            QCoreApplication.translate("RegisterForm", "     Email", None)
        )
        self.Password.setText(
            QCoreApplication.translate("RegisterForm", "     Password", None)
        )
        self.pushButton_register.setText(
            QCoreApplication.translate("RegisterForm", "Register", None)
        )
        self.pushButton_to_login.setText(
            QCoreApplication.translate("RegisterForm", "Already have an account?", None)
        )
        self.pushButton_to_login2.setText(
            QCoreApplication.translate("RegisterForm", "Login", None)
        )

    # retranslateUi
