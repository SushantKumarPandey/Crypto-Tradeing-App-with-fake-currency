import os
import sys
import json
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
from anyio.streams import file
from pyarrow import show_info
from werkzeug.security import generate_password_hash, check_password_hash
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from PyQt6.QtWidgets import QCheckBox


class Tutorialwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("tutorial.ui", self)
        self.tutorial_steps = []
        self.step = 0

        try:
            conn = sqlite3.connect("crypto.db")
            cursor = conn.cursor()

            cursor.execute("SELECT nameT, info from tutorial")
            self.tutorial_steps = cursor.fetchall()


        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "error", f"DB-eroor: {e}")
            self.tutorial_steps = [("errr", "no tutorials found")]

        finally:
            conn.close()

        self.update_tutorial()
        self.button_next.clicked.connect(self.next_step)
        self.button_back.clicked.connect(self.back_step)

    def update_tutorial(self):
        title, content = self.tutorial_steps[self.step]
        self.label_title.setText(title)
        self.label_content.setText(content)

    def next_step(self):
        self.step += 1
        if self.step < len(self.tutorial_steps):
            self.update_tutorial()
        else:
            self.accept()

    def back_step(self):
        self.step -= 1
        if self.step < len(self.tutorial_steps):
            self.update_tutorial()
        else:
            self.accept()


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
        try:
            conn = sqlite3.connect("crypto.db")
            cursor = conn.cursor()

            cursor.execute("SELECT name,price FROM coin WHERE symbol=?", (symbol,))
            name = cursor.fetchone()

            print(name)
            self.label.setText(name[0])
            self.label_2.setText(str(round(name[1],4)))
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

            c.execute(''' SELECT balance FROM user WHERE id = ?''', (self.user_id,))
            balance = c.fetchone()

            c.execute("SELECT price FROM coin WHERE symbol=?", (self.item,))
            price = c.fetchone()
            order = (amount*price[0])

            if balance[0] - order > 0:
                c.execute(''' INSERT INTO holding(user_id,coin_symbol,amount,value) VALUES (?,?,?,?) ''', (self.user_id, self.item , amount, order))
                c.execute(''' UPDATE user SET balance = ? WHERE id = ? ''', (balance[0]-order,self.user_id))

                c.execute(''' SELECT EXISTS(SELECT trades
                              FROM cryptos_to_watch
                              WHERE name = ?)''', (self.item,))
                trades = c.fetchone()
                print(trades)
                if trades[0] != 0:
                    trades = trades[0] + 1
                    c.execute(''' UPDATE cryptos_to_watch SET trades = ? WHERE name = ? ''', (trades,self.item))
                else:
                    trades = 1
                    c.execute(''' INSERT INTO cryptos_to_watch(name,trades) VALUES (?,?)''', (self.item,trades))
                    print("cryptos to watch added")
                QtWidgets.QMessageBox.information(
                    self, "Purchase Succesful", "The Crypto has been added to your Portfolio"
                )

            else:
                print("not enough money")
                QtWidgets.QMessageBox.information(
                    self, "Purchase Unsuccessful", "Requiered funds not available"
                )

            conn.commit()

        except sqlite3.Error as e:
            print("SQLite error:", e)

        except Exception as e:
            print("Unexpected error:", e)

        finally:
            conn.close()

    def sell_crypto(self):
        amount = self.spinBox.value()
        try:
            conn = sqlite3.connect('crypto.db')
            c = conn.cursor()

            c.execute(''' SELECT balance FROM user WHERE id = ?''', (self.user_id,))
            balance = c.fetchone()

            c.execute('''SELECT amount from holding Where user_id = ? AND coin_symbol = ?''', (self.user_id, self.item))
            current = c.fetchone()
            current = current[0] - amount

            c.execute("SELECT price FROM coin WHERE symbol=?", (self.item,))
            price = c.fetchone()

            restore = price[0] * amount
            rebalance = balance[0] + restore
            print(current)

            if current > 0:
                c.execute(''' UPDATE holding SET amount = ?, value = ? WHERE user_id = ? AND coin_symbol = ? ''', (current, current * price[0],self.user_id, self.item))
                c.execute(''' UPDATE user SET balance = ? WHERE id = ? ''', (rebalance, self.user_id))
                QtWidgets.QMessageBox.information(
                    self, "Sell Succesful", "The Crypto has been sold from your Portfolio"
                )
            else:
                QtWidgets.QMessageBox.information(
                    self, "Sell Unsuccesful", "insufficient amount of coins to sell"
                )
            conn.commit()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

        except sqlite3.Error as e:
            print("SQLite error:", e)

        finally:
            conn.close()


class Registerwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "register.ui")
        uic.loadUi(ui_path, self)

        self.pushButton_register.clicked.connect(self.register)

    def create_new_user(self, username, password, email, db_path="../client/crypto.db"):
        if username == "" or password == "" or email == "":
            return "empty"
        if "@" not in email or "." not in email:
            return "notValid"

        password

        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                """
                    INSERT INTO user (username, password, email, balance)
                    VALUES (?,?,?,?)
                """,
                (username, password, email, 10000),
            )
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
            (
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Enter a valid email address."
                )
            )
        elif result == "success":
            QtWidgets.QMessageBox.information(
                self,
                "Account created",
                "Your account has been created! You are now able to log in.",
            )
            self.close()


class Loginwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.current_user_id = None

        self.Register.clicked.connect(self.show_login)
        self.register_window = None
        self.mainwindow = None

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

            if user and user[1] == password:
                QtWidgets.QMessageBox.information(
                    self, "Login Success", "Successfully Logged In"
                )
                self.current_user_id = user[0]
                self.mainwindow = Mainwindow(self.current_user_id)
                self.mainwindow.show()
                self.close()
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Login Failed", "Invalid Username or Password"
                )
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
        if self.user_id is not None:
            self.loginButton.hide()
            self.get_profile_info()
        else:
            self.ask_tutorial()

        self.fetch_top_winners()
        self.fetch_top_losers()
        self.load_Tutorial_Guides()
        self.load_achievements()
        self.fetch_cryptos_to_watch()
        self.account_search()
        self.fetch_table()

        self.search.clicked.connect(self.account_search)
        self.loginButton.clicked.connect(self.login_show)
        self.Accounts.itemClicked.connect(self.show_account)
        self.Guides.itemClicked.connect(self.show_guides)
        self.Tutorial.itemClicked.connect(self.show_tutorial)
        self.Accounts_2.itemClicked.connect(self.crypto_show)
        self.refresh.clicked.connect(self.fetch_table)
        self.search_2.clicked.connect(self.crypto_search)
        self.updateButton.clicked.connect(self.get_profile_info)

        self.login_window = None
        self.crypto_window = None

    def ask_tutorial(self):
        asked = QtWidgets.QMessageBox.question(
            self,
            "start Tutorial?",
            "Do you want to beginn the tutorial?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if asked == QtWidgets.QMessageBox.StandardButton.Yes:
            self.start_tutorial()

    def start_tutorial(self):
        tutorial = Tutorialwindow()
        tutorial.exec()

    def login_show(self):
        self.login_window = Loginwindow()
        self.login_window.show()
        self.close()

    def crypto_show(self, item):
        symbol = item.text()
        try:
            self.crypto_window = Cryptowindow(
                item.text(), self.user_id
            )  # assume item is QListWidgetItem
            self.crypto_window.show()
        except Exception as e:
            print("❌ Error opening Cryptowindow:", e)

    def show_guides(self, item):
        guides_name = item.text()

        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(
                """
                    SELECT nameG, info FROM guides
                    WHERE nameG = ?
                """,
                (guides_name,),
            )
            one = c.fetchone()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

        if one:

            QtWidgets.QMessageBox.information(
                self,
                f"{one[0]}",
                f"{one[1]}",
            )

            QtWidgets.QMessageBox.information(self, f"{one[0]}", f"{one[1]}", )

        else:
            QtWidgets.QMessageBox.information(self, "Keine Daten", "help")

    def show_tutorial(self, item):
        tutorial_name = item.text()

        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(
                """
                    SELECT nameT, info FROM tutorial
                    WHERE nameT = ?
                """,
                (tutorial_name,),
            )
            one = c.fetchone()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

        if one:

            QtWidgets.QMessageBox.information(
                self,
                f"{one[0]}",
                f"{one[1]}",
            )
            QtWidgets.QMessageBox.information(self, f"{one[0]}", f"{one[1]}", )

        else:
            QtWidgets.QMessageBox.information(self, "Keine Daten", "help")

    def show_account(self, item):
        username = item.text()
        infos = []
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()
            c.execute(
                """
                    SELECT username, email FROM user
                    WHERE username = ?
                """,
                (username,),
            )
            infos = c.fetchall()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

        if infos:
            user_info = infos[0]
            QtWidgets.QMessageBox.information(
                self, "Account Info", f"Username: {user_info[0]}\nEmail: {user_info[1]}"
            )
        else:
            QtWidgets.QMessageBox.information(
                self, "Keine Daten", "Kein Benutzer gefunden."
            )

    def crypto_search(self):
        search_term = self.search_Account_3.text()
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(
                """
            SELECT symbol FROM coin Where symbol LIKE ?""",
                (f"%{search_term}%",),
            )

            results = c.fetchall()
            print(results)

            self.Accounts_2.clear()
            for row in results:
                item = QtWidgets.QListWidgetItem(row[0])
                self.Accounts_2.addItem(row[0])

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

    def get_profile_info(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "limit": "5",
            "convert": "EUR",
            "sort": "percent_change_24h",
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8bc7959e-153c-40dd-8da9-34e544661e71",
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data = response.json()

            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(''' SELECT username,balance FROM user WHERE id = ?''', (self.user_id,))
            username = c.fetchone()
            self.label_10.setText(str(username[0]))
            self.kontostand.display(username[1])
            self.kontostand_2.display(username[1])

            c.execute(''' SELECT coin_symbol,value FROM holding WHERE user_id = ?''', (self.user_id,))
            data = c.fetchall()

            for i,coin in enumerate(data):
                self.infos.setItem(i,0, QTableWidgetItem(str(coin[0])))
                self.infos.setItem(i,1, QTableWidgetItem(str(round(coin[1],4)) + '€'))

            for i,coin in enumerate(data):
                self.tableWidget_6.setItem(i,0, QTableWidgetItem(str(coin[0])))
                self.tableWidget_6.setItem(i,1, QTableWidgetItem(str(round(coin[1],4)) + '€'))

            conn.commit()

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

        finally:
            conn.close()

    def account_search(self):
        name = self.search_Account_2.text().strip()
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(
                """
            SELECT username FROM user
                WHERE username LIKE ?
            """,
                (f"%{name}%",),
            )

            results = c.fetchall()
            print(results)

            self.Accounts.clear()
            for row in results:
                item = QtWidgets.QListWidgetItem(row[0])
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

    def load_Tutorial_Guides(self):
        try:
            conn = sqlite3.connect("crypto.db")
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
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {"limit": "500", "convert": "EUR"}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8bc7959e-153c-40dd-8da9-34e544661e71",
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data = response.json()

            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(
                """DELETE
                         FROM coin"""
            )

            for coin in data["data"]:
                name = coin["name"]
                symbol = coin["symbol"]
                supply = coin["total_supply"]
                last_updated = coin["last_updated"]
                price = coin["quote"]["EUR"]["price"]
                market_cap = coin["quote"]["EUR"]["market_cap"]

                c.execute(
                    """
                    INSERT INTO coin (id, price, name, supply, symbol, market_cap, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        str(coin["id"]),
                        float(price),
                        name,
                        float(supply),
                        symbol,
                        float(market_cap),
                        last_updated,
                    ),
                )
                self.Accounts_2.addItem(symbol)

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)
        except Exception as e:
            print("Other error:", e)

    def fetch_top_winners(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "limit": "7",
            "convert": "EUR",
            "sort": "percent_change_24h",
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8bc7959e-153c-40dd-8da9-34e544661e71",
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data = response.json()

            i = 0
            for coin in data["data"]:
                self.tableWidget_3.setItem(i, 0, QTableWidgetItem(coin["name"]))
                self.tableWidget_3.setItem(
                    i, 1, QTableWidgetItem(str(round(coin["quote"]["EUR"]["price"], 4)) + '€')
                )
                self.tableWidget_3.setItem(
                    i,
                    2,
                    QTableWidgetItem('+' + str(round(coin["quote"]["EUR"]["percent_change_24h"], 4)) + '%'),
                )
                i = i + 1

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

    def fetch_top_losers(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "limit": "100",
            "convert": "EUR",
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8bc7959e-153c-40dd-8da9-34e544661e71",
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)

            data = response.json()

            if "data" not in data:
                print("API error or malformed response")
                return

            sorted_coins = sorted(
                data["data"], key=lambda x: x["quote"]["EUR"]["percent_change_24h"]
            )

            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            for i, coin in enumerate(sorted_coins[:7]):
                self.tableWidget_4.setItem(i, 0, QTableWidgetItem(coin["name"]))
                self.tableWidget_4.setItem(
                    i, 1, QTableWidgetItem(str(round(coin["quote"]["EUR"]["price"],4)) + '€')
                )
                self.tableWidget_4.setItem(
                    i,
                    2,
                    QTableWidgetItem(str(round(coin["quote"]["EUR"]["percent_change_24h"],4)) + '%'),
                )
                print(coin["name"])

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

    def fetch_cryptos_to_watch(self):
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(''' SELECT * FROM cryptos_to_watch''')
            data = c.fetchall()

            for i,coin in enumerate(data):
                self.tableWidget_5.setItem(i,0, QTableWidgetItem(str(coin[1])))
                self.tableWidget_5.setItem(i,1, QTableWidgetItem(str(coin[2])))

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

    def load_achievements(self):
        achievements = [
            "✅ Completed your first trade",
            "📈 Portfolio above 1000",
            "🔥 Daily login streak",
            "💼 10 days of activity",
            "⏳ In Progress",
        ]

        container = self.findChild(QtWidgets.QWidget, "achievementsContainer")
        if container:
            layout = container.layout()
            for text in achievements:
                checkbox = QtWidgets.QCheckBox(text)
                checkbox.setStyleSheet(
                    """
                    QCheckBox {
                        font: 14pt "Segoe UI";
                        color: rgb(108, 216, 160);
                    }
                """
                )
                checkbox.setChecked("✅" in text or "🔥" in text)
                layout.addWidget(checkbox)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow(None)
    window.show()
    sys.exit(app.exec())
