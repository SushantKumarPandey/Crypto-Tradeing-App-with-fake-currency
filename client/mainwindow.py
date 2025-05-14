import sys
from dbm import sqlite3

from PyQt6 import QtWidgets, uic
from werkzeug.security import check_password_hash


class Registerwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("register.ui", self)


class Loginwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)

        self.pushButton_to_login.clicked.connect(self.verify_login)

    def verify_login(self):

        username = self.lineEdit_password_2.text()
        password = self.lineEdit_password.text()

        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()
            c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            conn.close()

            if user and check_password_hash(user[1], password):
                QtWidgets.QMessageBox.information(self, "Login Success", "Successfully Logged In")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid Username or Password")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")



class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)

        self.loginButton.clicked.connect(self.login_show)
        self.login_window = None

    def login_show(self):
        self.login_window = Loginwindow()
        self.login_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec())

