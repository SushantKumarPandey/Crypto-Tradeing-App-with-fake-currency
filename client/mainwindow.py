import os
import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
from werkzeug.security import generate_password_hash, check_password_hash
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class Cryptowindow(QtWidgets.QWidget):
    def __init__(self, item_text, user_id):
        super().__init__()
        uic.loadUi("crypto.ui", self)
        self.item = item_text
        self.user_id = user_id

        self.show_info()
        self.pushButton.clicked.connect(self.buy_crypto)
        self.pushButton_2.clicked.connect(self.sell_crypto)

    def show_info(self):
        symbol = self.item
        print('before' + symbol)
        try:
            conn = sqlite3.connect("crypto.db")
            cursor = conn.cursor()

            cursor.execute("SELECT name,price FROM coin WHERE symbol=?", (symbol,))
            name = cursor.fetchone()

            print(name)
            self.label.setText(name[0])
            self.label_2.setText(str(name[1]))
            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)
        except Exception as e:
            print("Other error:", e)

    def buy_crypto(self):
        amount = self.spinBox.value()
        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute(''' INSERT INTO holding VALUES (?,?,?) ''',
                      (self.user_id, self.item, amount))

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

    def sell_crypto(self):
        amount = self.spinBox.value()
        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute('''SELECT amount from holding Where user_id=? AND coin_symbol=?''',
                      (self.user_id, self.item))
            current = c.fetchone()
            current = current - amount

            c.execute(''' DELETE FROM HOLDING WHERE coin_symbol=? AND user_id=?''',
                      (self.item, self.user_id))

            c.execute(''' INSERT INTO holding VALUES (?,?,?) ''',
                      (self.user_id, self.item, current))

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)


class Registerwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "register.ui")
        uic.loadUi(ui_path, self)

        self.pushButton_register.clicked.connect(self.register)

    def create_new_user(self, username, password, email, db_path="../client/crypto.db"):
        if username == '' or password == '' or email == '':
            return "empty"
        if '@' not in email or '.' not in email:
            return "notValid"

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('''
                    INSERT INTO user (username, password, email)
                    VALUES (?,?,?)
                ''', (username, hashed_password, email))
            conn.commit()
            self.close()
            return "success"

        except sqlite3.Error as e:
            if f"{e}" == "UNIQUE constraint failed: user.username":
                QtWidgets.QMessageBox.warning(self, "Error", "Username already in use.")
            else:
                print(f"SQLite Error: {e}")
                QtWidgets.QMessageBox.warning(self, "Error", f"SQLite Error: {e}")

        finally:
            conn.close()

    def register(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        email = self.lineEdit_email.text()

        result = self.create_new_user(username, password, email)

        if result == "empty":
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields")
        elif result == "notValid":
            QtWidgets.QMessageBox.warning(self, "Error", "Enter a valid email address.")
        elif result == "success":
            QtWidgets.QMessageBox.information(self, 'Account created',
                                              "Your account has been created! You are now able to log in.")
            self.close()

class Loginwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.current_user_id = None

        self.Register.clicked.connect(self.show_login)
        self.register_window = None

        self.pushButton_to_login.clicked.connect(self.verify_login)

    def verify_login(self):

        username = self.lineEdit_password_2.text()
        password = self.lineEdit_password.text()

        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()
            c.execute("SELECT id, password FROM user WHERE username = ?", (username,))
            user = c.fetchone()
            conn.close()

            if user and check_password_hash(user[1], password):
                QtWidgets.QMessageBox.information(
                    self, "Login Success", "Successfully Logged In"
                )
                self.current_user_id = user['id']
                self.accept()
                self.mainwindow = Mainwindow(self.current_user_id)
                self.mainwindow.show()
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid Username or Password")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def show_login(self):
        self.register_window = Registerwindow()
        self.register_window.show()


class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("form.ui", self)
        self.user_id = user_id

        self.fetch_top_winners()
        self.fetch_top_losers()

        self.loade_Tutorial_Guides()
        self.search.clicked.connect(self.account_search)
        self.loginButton.clicked.connect(self.login_show)
        self.Accounts.itemClicked.connect(self.show_account)
        self.Guides.itemClicked.connect(self.show_guides)
        self.Tutorial.itemClicked.connect(self.show_tutorial)
        self.Accounts_2.itemClicked.connect(self.crypto_show)
        self.refresh.clicked.connect(self.fetch_table)
        self.search_2.clicked.connect(self.crypto_search)
        self.login_window = None
        self.crypto_window = None

    def login_show(self):
        self.login_window = Loginwindow()
        self.login_window.show()

    def crypto_show(self, item):
        try:
            self.crypto_window = Cryptowindow(item.text(), self.user_id)  # assume item is QListWidgetItem
            self.crypto_window.show()
        except Exception as e:
            print("❌ Error opening Cryptowindow:", e)

    def show_guides(self, item):
        guides_name = item.text()

        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute("""
                    SELECT nameG, info FROM guides
                    WHERE nameG = ?
                """, (guides_name,))
            one = c.fetchone()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

        if one:
            QtWidgets.QMessageBox.information(self, f"{one[0]}", f"{one[1]}",)
        else:
            QtWidgets.QMessageBox.information(self, "Keine Daten", 'help')

    def show_tutorial(self, item):
        tutorial_name = item.text()

        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute("""
                    SELECT nameT, info FROM tutorial
                    WHERE nameT = ?
                """, (tutorial_name,))
            one = c.fetchone()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

        if one:
            QtWidgets.QMessageBox.information(self, f"{one[0]}", f"{one[1]}",)
        else:
            QtWidgets.QMessageBox.information(self, "Keine Daten", 'help')

    def show_account(self, item):
        username = item.text()
        infos = []
        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()
            c.execute("""
                    SELECT username, email FROM user
                    WHERE username = ?
                """, (username,))
            infos = c.fetchall()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

        if infos:
            user_info = infos[0]
            QtWidgets.QMessageBox.information(
                self,
                "Account Info",
                f"Username: {user_info[0]}\nEmail: {user_info[1]}"
            )
        else:
            QtWidgets.QMessageBox.information(self, "Keine Daten", "Kein Benutzer gefunden.")

    def crypto_search(self):
        search_term = self.search_Account_3.text()
        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute('''
            SELECT symbol FROM coin Where symbol LIKE ?''', (f'%{search_term}%',))

            results = c.fetchall()
            print(results)

            self.Accounts_2.clear()
            for row in results:
                self.Accounts_2.addItem(row[0])

        except sqlite3.Error as e:

            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:

            conn.close()

    def account_search(self):
        name = self.search_Account_2.text().strip()
        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute("""
            SELECT username FROM user
                WHERE username LIKE ?
            """, (f"%{name}%",))

            results = c.fetchall()
            print(results)

            self.Accounts.clear()
            for row in results:
                self.Accounts.addItem(row[0])

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

    """
        def crypto_search(self):
            name = self.search_Account_2.text().strip()

            try:
                conn = sqlite3.connect('crypto.db')
                c = conn.cursor()

                results = c.fetchall()
                print(results)

                self.Crypto.clear()
                for row in results:
                    item = QtWidgets.QListWidgetItem(row[0])
                    self.Crypt.addItem(row[0])

            except sqlite3.Error as e:
                QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

            finally:
                conn.close()
    """

    def loade_Tutorial_Guides(self):

        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            self.Guides.clear()
            c.execute("SELECT nameG FROM guides")
            all_guides = c.fetchall()
            for row in all_guides:
                self.Guides.addItem(row[0])

            self.Tutorial.clear()
            c.execute("SELECT nameT FROM tutorial")
            all_tutorials = c.fetchall()
            for row in all_tutorials:
                self.Tutorial.addItem(row[0])

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

    """
        def show_crypto(self, item):
           name = item.text()
           QtWidgets.QMessageBox.information(self, f"name: {name}")
    """

    def fetch_table(self):
        url = ("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest")
        parameters = {
            'limit': '500',
            'convert': 'EUR'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '8bc7959e-153c-40dd-8da9-34e544661e71'
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data = response.json()

            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute('''DELETE
                         FROM coin''')

            for coin in data['data']:
                name = coin['name']
                symbol = coin['symbol']
                supply = coin['total_supply']
                last_updated = coin['last_updated']
                price = coin['quote']['EUR']['price']
                market_cap = coin['quote']['EUR']['market_cap']

                c.execute('''
                    INSERT INTO coin (id, price, name, supply, symbol, market_cap, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(coin['id']),
                    float(price),
                    name,
                    float(supply),
                    symbol,
                    float(market_cap),
                    last_updated
                ))
                self.Accounts_2.addItem(symbol)

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)
        except Exception as e:
            print("Other error:", e)

    def fetch_top_winners(self):
        url = ("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest")
        parameters = {
            'limit': '5',
            'convert': 'EUR',
            'sort': 'percent_change_24h',
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '8bc7959e-153c-40dd-8da9-34e544661e71'
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data = response.json()

            conn = sqlite3.connect('crypto.db')

            i = 0
            for coin in data['data']:
                self.tableWidget_3.setItem(i, 0, QTableWidgetItem(coin['name']))
                self.tableWidget_3.setItem(i, 1, QTableWidgetItem(str(coin['quote']['EUR']['price'])))
                self.tableWidget_3.setItem(i, 2, QTableWidgetItem(str(coin['quote']['EUR']['percent_change_24h'])))
                i = i+1
                print(coin['name'])

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

    def fetch_top_losers(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            'limit': '100',
            'convert': 'EUR',
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '8bc7959e-153c-40dd-8da9-34e544661e71'
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            print(response.status_code)
            print(response.text)  # Debugging line

            data = response.json()

            if 'data' not in data:
                print("API error or malformed response")
                return

            sorted_coins = sorted(
                data['data'],
                key=lambda x: x['quote']['EUR']['percent_change_24h']
            )

            conn = sqlite3.connect('crypto.db')

            for i, coin in enumerate(sorted_coins[:5]):
                self.tableWidget_4.setItem(i, 0, QTableWidgetItem(coin['name']))
                self.tableWidget_4.setItem(i, 1, QTableWidgetItem(str(coin['quote']['EUR']['price'])))
                self.tableWidget_4.setItem(i, 2, QTableWidgetItem(str(coin['quote']['EUR']['percent_change_24h'])))
                print(coin['name'])

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow(None)
    window.show()
    sys.exit(app.exec())
