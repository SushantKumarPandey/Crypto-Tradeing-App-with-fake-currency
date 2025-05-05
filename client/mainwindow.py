import sys
from PyQt6 import QtWidgets, uic

class Registerwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("register.ui", self)

class Loginwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)

        self.Register.clicked.connect(self.show_login)
        self.register_window = None

    def show_login(self):
        self.register_window = Registerwindow()
        self.register_window.show()

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

