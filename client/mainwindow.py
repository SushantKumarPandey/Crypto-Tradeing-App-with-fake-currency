import sys
import json
import sqlite3

from PyQt6 import QtWidgets, uic
from werkzeug.security import generate_password_hash
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

class Registerwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("register.ui", self)

        self.pushButton_register.clicked.connect(self.register)

    def register(self):

        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        email = self.lineEdit_email.text()

        hashed_password = generate_password_hash(password)

        if username == '' or password == '' or email == '':
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        try:
            print('connecting ...')
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()
            print('Executing Insert')

            c.execute('''
                    INSERT INTO user (username, password, email) 
                    VALUES (?,?,?)
                ''', (username, hashed_password, email))
            conn.commit()
            print('Insert done')
            QtWidgets.QMessageBox.information(self, 'Account created',
                                              "Your account has been created! You are now able to log in.")
            self.close()

        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"SQLite Error: {e}")

        finally:
            conn.close()


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
        self.Accounts_2.itemClicked.connect(self.fetch_table())
        self.login_window = None

    def login_show(self):
        self.login_window = Loginwindow()
        self.login_window.show()

    def fetch_table(self, item):
        coinName = item.text()
        url = ("https://pro-api.coinmarketcap.com/v1/cryptocurrency/map")
        parameters = {
            'symbol' : coinName,
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '8bc7959e-153c-40dd-8da9-34e544661e71'
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec())