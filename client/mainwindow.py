import os
import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


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

    """
    update_tutorial: lädt die derzeitige Page im Tutorial
    """

    def update_tutorial(self):
        title, content = self.tutorial_steps[self.step]
        self.label_title.setText(title)
        self.label_content.setText(content)

    """
    next_step: lässt einen eine Page im Tutorial vorangehen
    """

    def next_step(self):
        self.step += 1
        if self.step < len(self.tutorial_steps):
            self.update_tutorial()
        else:
            self.accept()

    """
    back_step: lässt einen eine Page im Tutorial zurückgehen
    """

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

    """
    show_info: eine Methode, welche den Namen,
    und den derzeitigen Wert der Crypto abruft und darstellt
    """

    def show_info(self):
        symbol = self.item
        try:
            conn = sqlite3.connect("crypto.db")
            cursor = conn.cursor()

            cursor.execute("SELECT name,price FROM coin WHERE name=?", (symbol,))
            name = cursor.fetchone()

            print(name)
            self.label.setText(name[0])
            self.label_2.setText(str(round(name[1], 4)))
            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)
        except Exception as e:
            print("Other error:", e)

    """
    buy_crypto: die Methode, welche den Kaufprozess nach dem drücken des buy
    Buttons verarbeitet.
    fügt die eingegebene Anzahl in das Portfolio ein.
    fügt dazu auch noch ein Eintrag in cryptos_to_watch hinzu
    """

    def buy_crypto(self):
        amount = self.spinBox.value()
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(""" SELECT balance FROM user WHERE id = ?""", (self.user_id,))
            balance = c.fetchone()

            c.execute("SELECT price,symbol FROM coin WHERE name=?", (self.item,))
            price = c.fetchone()
            order = amount * price[0]

            c.execute(
                """SELECT coin_symbol,amount,value
                         FROM holding
                         WHERE coin_symbol = ?""",
                (price[1],),
            )
            exists = c.fetchone()
            print(exists)

            if balance[0] - order > 0 and amount > 0:
                if exists is None:
                    c.execute(
                        """ INSERT INTO holding(user_id,
                                                coin_symbol,
                                                amount,
                                                value)
                                  VALUES (?,?,?,?) """,
                        (self.user_id, price[1], amount, order),
                    )
                else:
                    c.execute(
                        """UPDATE holding SET amount = ?, value = ?
                                 WHERE coin_symbol = ?""",
                        (exists[1] + amount, exists[2] + order, price[1]),
                    )

                c.execute(
                    """ UPDATE user
                              SET balance = ?
                              WHERE id = ? """,
                    (balance[0] - order, self.user_id),
                )
                c.execute(
                    """ SELECT EXISTS(SELECT trades
                              FROM cryptos_to_watch
                              WHERE name = ?)""",
                    (self.item,),
                )
                trades = c.fetchone()
                print(trades)
                if trades[0] != 0:
                    trades = trades[0] + 1
                    c.execute(
                        """ UPDATE cryptos_to_watch
                            SET trades = ?
                            WHERE name = ? """,
                        (trades, self.item),
                    )
                else:
                    trades = 1
                c.execute(
                    """ INSERT INTO cryptos_to_watch(name,trades)
                        VALUES (?,?)""",
                    (self.item, trades),
                )
                print("cryptos to watch added")
                QtWidgets.QMessageBox.information(
                    self,
                    "Purchase Succesful",
                    "The Crypto has been added to your Portfolio",
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

    """
    sell_crypto: die Methode, welche den Verkaufsprozess nach dem drücken des sell buttons verarbeitet.
    entfernt entweder den Eintrag, oder passt die anzahl an Tokens im Portfolio an.
    """

    def sell_crypto(self):
        amount = self.spinBox.value()
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(""" SELECT balance FROM user WHERE id = ?""", (self.user_id,))
            balance = c.fetchone()

            c.execute(""" SELECT symbol,price FROM coin WHERE name = ?""", (self.item,))
            symbol = c.fetchone()

            c.execute(
                """SELECT amount from holding
                    Where user_id = ? AND coin_symbol = ?""",
                (self.user_id, symbol[0]),
            )
            current = c.fetchone()
            current = current[0] - amount
            restore = symbol[1] * amount
            rebalance = balance[0] + restore
            print(current)

            if current > 0:
                c.execute(
                    """ UPDATE holding SET amount = ?, value = ?
                        WHERE user_id = ? AND coin_symbol = ? """,
                    (current, current * symbol[1], self.user_id, symbol[0]),
                )
                c.execute(
                    """ UPDATE user SET balance = ? WHERE id = ? """,
                    (rebalance, self.user_id),
                )
                QtWidgets.QMessageBox.information(
                    self,
                    "Sell Succesful",
                    "The Crypto has been sold from your Portfolio",
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
        self.current_user_id = None

        self.Login.clicked.connect(self.show_login)
        self.login_window = None
        self.mainwindow = None

        self.pushButton_register.clicked.connect(self.register)

    """
    create_new_user: Erstellt einen neuen User in der Db, nachdem man die Daten eingegeben hat im Register Window,
    und den Button gepresst hat
    """

    def create_new_user(self, username, password, email, db_path="crypto.db"):
        if username == "" or password == "" or email == "":
            return "empty"
        if "@" not in email or "." not in email:
            return "notValid"

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

    """
    register: Verarbeitet den Register Button Press, und sendet die infos an die create_new_user Methode
    """

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
            self.mainwindow = Mainwindow(None)
            self.mainwindow.show()
            self.close()

    """
    show_login: führt einen zum login window, wenn man doch bereits einen Account hat
    """

    def show_login(self):
        self.login_window = Loginwindow()
        self.login_window.show()


class Loginwindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.current_user_id = None

        self.Register.clicked.connect(self.show_register)
        self.register_window = None
        self.mainwindow = None

        self.pushButton_to_login.clicked.connect(self.verify_login)

    """
    verify_login: prüft die Eingegebenen Daten mit der Db, wenn sie übereinstimmen, wird der login durchgeführt
    """

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

    """
    show_register: Wenn man keinen Account besitzt, wird man durch diese Methode auf das Register window, verwiesen
    """

    def show_register(self):
        self.register_window = Registerwindow()
        self.register_window.show()


class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        uic.loadUi("form.ui", self)

        self.fetch_top_winners()
        self.fetch_top_losers()
        self.load_tutorial_guides()
        self.load_achievements()
        self.fetch_cryptos_to_watch()
        self.account_search()
        self.fetch_table()

        if self.user_id is not None:
            self.loginButton.hide()
            self.registerButton.hide()
            self.get_profile_info()
            self.tabWidget.setTabVisible(5, True)
        else:
            self.ask_tutorial()
            self.tabWidget.setTabVisible(5, False)

        self.search.clicked.connect(self.account_search)
        self.loginButton.clicked.connect(self.login_show)
        self.registerButton.clicked.connect(self.register_show)
        self.Accounts.itemClicked.connect(self.show_account)
        self.Guides.itemClicked.connect(self.show_guides)
        self.Tutorial.itemClicked.connect(self.show_tutorial)
        self.Accounts_2.itemClicked.connect(self.crypto_show)
        self.refresh.clicked.connect(self.fetch_table)
        self.search_2.clicked.connect(self.crypto_search)
        self.updateButton.clicked.connect(self.get_profile_info)

        self.login_window = None
        self.register_window = None
        self.crypto_window = None

    """
    ask_tutorial: fragt am Start des Programmes, ob man das Tutorial machen will.
    Wenn man ja klickt, lädt es das Tutorial
    """

    def ask_tutorial(self):
        asked = QtWidgets.QMessageBox.question(
            self,
            "start Tutorial?",
            "Do you want to beginn the tutorial?",
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
        )

        if asked == QtWidgets.QMessageBox.StandardButton.Yes:
            self.start_tutorial()

    """
    start_tutorial: Zeigt das Tutorial an
    """

    def start_tutorial(self):
        tutorial = Tutorialwindow()
        tutorial.exec()

    """
    login_show: lädt die Login Page aus dem Mainwindow, nach dem man den Login Button klickt
    """

    def login_show(self):
        self.login_window = Loginwindow()
        self.login_window.show()
        self.close()

    """
    register_show: lädt die Register Page aus dem Mainwindow, nachdem man den Register Button klickt
    """

    def register_show(self):
        self.register_window = Registerwindow()
        self.register_window.show()
        self.close()

    """
    load_achievements: lädt die Achievements Liste
    """

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

    """
    crypto_show: macht die einzelnen Cryptos clickable und öffnet das Crypto_window
    """

    def crypto_show(self, item):
        try:
            self.crypto_window = Cryptowindow(item.text(), self.user_id)
            self.crypto_window.show()
        except Exception as e:
            print("❌ Error opening Cryptowindow:", e)

    """
    show_guides:zeigt die Guides aus der DB an, und macht sie einsehbar nach dem anclicken
    """

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

            QtWidgets.QMessageBox.information(
                self,
                f"{one[0]}",
                f"{one[1]}",
            )

        else:
            QtWidgets.QMessageBox.information(self, "Keine Daten", "help")

    """
    show_tutorial: lässt das Tutorial beim erst Start des Programmes aufrufen.
    """

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
            QtWidgets.QMessageBox.information(
                self,
                f"{one[0]}",
                f"{one[1]}",
            )

        else:
            QtWidgets.QMessageBox.information(self, "Keine Daten", "help")

    """
    show_account: zeigt infos über einen User, welche nach dem click auf ihren Namen angezeigt wird
    """

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

    """
    crypto_search: Methode, welche den String aus dem Search field nimmt,
    um die Crypto Liste nach dem passenden Token zu durchsuchen
    """

    def crypto_search(self):
        search_term = self.search_Account_3.text()
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(
                """
            SELECT name FROM coin Where name LIKE ? AND last_updated LIKE ?""",
                (f"%{search_term}%", self.current_time),
            )

            results = c.fetchall()
            print(results)

            self.Accounts_2.clear()
            for row in results:
                self.Accounts_2.addItem(row[0])

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

    """
    get_profile_info: Methode, welche die Datenbank für Profile Informationen absucht, um den Namen und Portfolio,
    sowie die derzeitige Balance einzufügen
    """

    def get_profile_info(self):
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8bc7959e-153c-40dd-8da9-34e544661e71",
        }
        session = Session()
        session.headers.update(headers)
        try:

            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(
                """ SELECT username,balance FROM user WHERE id = ?""", (self.user_id,)
            )
            username = c.fetchone()
            self.label_10.setText(str(username[0]))
            self.kontostand.display(username[1])
            self.kontostand_2.display(username[1])

            c.execute(
                """ SELECT coin_symbol,value,amount FROM holding WHERE user_id = ?""",
                (self.user_id,),
            )
            datas = c.fetchall()

            for i, coin in enumerate(datas):
                symbol = coin[0]
                value = coin[1]
                amount = coin[2]

                c.execute(
                    "SELECT price FROM coin WHERE symbol = ?",
                    (symbol,),
                )
                current_price = c.fetchone()

                if current_price is None:
                    price = 1
                else:
                    price = current_price[0]

                # Display data
                self.infos.setItem(i, 0, QTableWidgetItem(symbol))
                self.infos.setItem(i, 1, QTableWidgetItem(f"{round(value, 4)} €"))
                self.infos.setItem(
                    i,
                    2,
                    QTableWidgetItem(
                        str(round((((price * amount) - coin[1]) / coin[1]) * 100, 5))
                        + "%"
                    ),
                )
                self.infos.setItem(
                    i,
                    3,
                    QTableWidgetItem(str(round((price * amount) - coin[1], 5)) + "€"),
                )

            for i, coin in enumerate(datas):
                amount = coin[2]
                symbol = coin[0]

                c.execute(
                    "SELECT price FROM coin WHERE symbol = ?",
                    (symbol,),
                )
                current_price = c.fetchone()

                if current_price is None:
                    price = 1
                else:
                    price = current_price[0]
                self.tableWidget_6.setItem(i, 0, QTableWidgetItem(str(coin[0])))
                self.tableWidget_6.setItem(
                    i, 1, QTableWidgetItem(str(round(coin[1], 4)) + "€")
                )
                self.tableWidget_6.setItem(
                    i,
                    2,
                    QTableWidgetItem(
                        str(round((((price * amount) - coin[1]) / coin[1]) * 100, 5))
                        + "%"
                    ),
                )

            conn.commit()

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

        finally:
            conn.close()

    """
    account_ssearch: Methode, welche den String aus dem Search field nimmt,
    und in der Liste nach einem zutreffenden Account sucht
    """

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
                self.Accounts.addItem(row[0])

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

        finally:
            conn.close()

    """
    load_tutorial_guides: lädt die Guides und Tutorials in die Tabellen, woraus man sie dann abrufen kann
    """

    def load_tutorial_guides(self):
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
    fetch_table: ruft die Api ab, um die 300 größten Crypto tokens abzufragen.
    Die Methode fügt diese dann in die Liste in Search ein
    """

    def fetch_table(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {"limit": "300", "convert": "EUR"}
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

            c.execute(""" SELECT * FROM coin""")
            existing_coins = c.fetchall()
            print(existing_coins)

            if not existing_coins:
                for coin in data["data"]:
                    name = coin["name"]
                    symbol = coin["symbol"]
                    supply = coin["total_supply"]
                    last_updated = coin["last_updated"]
                    price = coin["quote"]["EUR"]["price"]
                    market_cap = coin["quote"]["EUR"]["market_cap"]

                    c.execute(
                        """
                        INSERT INTO coin (coin_id,
                                        price,
                                        name,
                                        supply,
                                        symbol,
                                        market_cap,
                                        last_updated)
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
                    self.Accounts_2.addItem(name)
                    self.current_time = last_updated
            else:
                for coin in data["data"]:
                    name = coin["name"]
                    symbol = coin["symbol"]
                    supply = coin["total_supply"]
                    last_updated = coin["last_updated"]
                    price = coin["quote"]["EUR"]["price"]
                    market_cap = coin["quote"]["EUR"]["market_cap"]

                    c.execute(
                        """
                            UPDATE coin SET
                                              price = ?,
                                              name = ?,
                                              supply = ?,
                                              symbol = ?,
                                              market_cap = ?,
                                              last_updated = ? WHERE coin_id = ?
                            """,
                        (
                            float(price),
                            name,
                            float(supply),
                            symbol,
                            float(market_cap),
                            last_updated,
                            str(coin["id"]),
                        ),
                    )
                    self.Accounts_2.addItem(name)
                    self.current_time = last_updated

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)
        except Exception as e:
            print("Other error:", e)

    """
    fetch_top_winners: ruft die api ab, und sucht dabei nach den tokens, die den größten 24h_change hatten
    """

    def fetch_top_winners(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "limit": "10",
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
                    i,
                    1,
                    QTableWidgetItem(
                        str(round(coin["quote"]["EUR"]["price"], 4)) + "€"
                    ),
                )
                self.tableWidget_3.setItem(
                    i,
                    2,
                    QTableWidgetItem(
                        "+"
                        + str(round(coin["quote"]["EUR"]["percent_change_24h"], 4))
                        + "%"
                    ),
                )
                i = i + 1

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

    """
    fetch_top_losers: ruft die api ab , und sucht dabei nach den tokens, die den größten 24h_change defizit verzeichnen
    """

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

            for i, coin in enumerate(sorted_coins[:10]):
                self.tableWidget_4.setItem(i, 0, QTableWidgetItem(coin["name"]))
                self.tableWidget_4.setItem(
                    i,
                    1,
                    QTableWidgetItem(
                        str(round(coin["quote"]["EUR"]["price"], 4)) + "€"
                    ),
                )
                self.tableWidget_4.setItem(
                    i,
                    2,
                    QTableWidgetItem(
                        str(round(coin["quote"]["EUR"]["percent_change_24h"], 4)) + "%"
                    ),
                )

            conn.commit()
            conn.close()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)

    """
    Cryptos to Watch: Ruft die "Cryptos to Watch" table ab und füllt sie in eine Table.
    Cryptos to watch sind alle kaüfe die getätigt wurden für die Jeweiligen Tokens. Soll dem User eine Idee gaben,
    welche Tokens gerade beliebt sind
    """

    def fetch_cryptos_to_watch(self):
        try:
            conn = sqlite3.connect("crypto.db")
            c = conn.cursor()

            c.execute(""" SELECT * FROM cryptos_to_watch""")
            data = c.fetchall()

            for i, coin in enumerate(data):
                self.tableWidget_5.setItem(i, 0, QTableWidgetItem(str(coin[1])))
                self.tableWidget_5.setItem(i, 1, QTableWidgetItem(str(coin[2])))

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("Request error:", e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow(None)
    window.show()
    sys.exit(app.exec())
