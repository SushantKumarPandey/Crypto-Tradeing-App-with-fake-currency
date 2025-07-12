import os
import sqlite3
import unittest

from client.mainwindow import Registerwindow
from werkzeug.security import check_password_hash, generate_password_hash
from PyQt6.QtWidgets import QApplication
from unittest.mock import patch
import sys
import atexit

app = QApplication.instance()
if not app:
    app = QApplication(
        sys.argv
    )  # Einmalig vor allen Tests, z.B. ganz oben in der Datei
atexit.register(app.quit)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
testDB = os.path.abspath(os.path.join(BASE_DIR, "..", "client", "crypto.db"))


class TestDB(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(testDB)
        self.c = self.conn.cursor()

        self.c.execute(
            """
         CREATE TABLE IF NOT EXISTS user(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT UNIQUE NOT NULL,
         password TEXT NOT NULL,
         email TEXT NOT NULL
         )
     """
        )
        self.c.execute("DELETE FROM user WHERE username = ?", ("tester",))
        self.c.execute(
            "INSERT INTO user (username, password, email, balance) VALUES (?, ?, ?,?)",
            ("tester", "password", "bsp@email.com", 10000),
        )
        self.c.execute(
            "INSERT OR IGNORE INTO user (username, password, email) VALUES (?, ?, ?)",
            ("kiki", "quack", "bsp1@gmail.com"),
        )
        self.c.execute(
            "INSERT OR IGNORE INTO user (username, password, email,balance) VALUES (?, ?, ?,?)",
            ("safe", generate_password_hash("safe"), "safe@test.de", 10000),
        )
        self.conn.commit()

    def test_connected(self):
        try:
            self.conn.execute("SELECT 1")
            state = "Connected"
        except Exception:
            state = "Disconnected"
        self.assertEqual(state, "Connected")

    def test_getUsers(self):
        self.c.execute("SELECT username FROM user WHERE username =  ?", ("tester",))
        user = self.c.fetchone()
        assert user is not None
        assert user[0] == "tester"

    def test_password_fromUser(self):
        self.c.execute("SELECT password FROM user WHERE username = 'kiki' ")
        password = self.c.fetchone()[0]
        self.assertEqual(password, "quack")

    def test_hasedPassword(self):
        self.c.execute("SELECT password FROM user WHERE username = 'safe' ")
        hashed_password = self.c.fetchone()[0]
        password = "safe"

        self.assertNotEqual(hashed_password, "safe")
        self.assertTrue(check_password_hash(hashed_password, password))

    def test_email_fromUser(self):
        self.c.execute("SELECT email FROM user WHERE username = 'kiki' ")
        email = self.c.fetchone()[0]
        self.assertEqual(email, "bsp1@gmail.com")

        self.conn.close()


TEST_DB_PATH = os.path.abspath("test_crypto.db")


class TestHTTP(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(TEST_DB_PATH)
        self.c = self.conn.cursor()

        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            balance FLOAT NOT NULL
            )
        """
        )
        self.c.execute("DELETE FROM user WHERE username = ?", ("tee",))
        self.c.execute("DELETE FROM user WHERE username = ?", ("user",))
        self.conn.commit()
        # self.conn.close()
        self.window = Registerwindow()

    @patch("client.mainwindow.QtWidgets.QMessageBox.warning")
    @patch("client.mainwindow.QtWidgets.QMessageBox.information")
    @patch("client.mainwindow.Loginwindow.show")
    def test_createUser(self, mock_show, mock_info, mock_warn):
        new_user = self.window.create_new_user(
            "tee", "secure", "email@example.com", db_path=TEST_DB_PATH
        )
        self.assertEqual(new_user, "success")

    @patch("client.mainwindow.QtWidgets.QMessageBox.warning")
    def test_usernameUnique(self, mock_warn):
        conn = sqlite3.connect(TEST_DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO user (username, password, email, balance) VALUES (?, ?, ?, ?)",
            ("tester", "password", "bsp@email.com", 10000),
        )
        conn.commit()
        conn.close()
        result = self.window.create_new_user(
            "tester", "secure", "email@example.com", db_path=TEST_DB_PATH
        )
        self.assertIsNone(result)

    @patch("client.mainwindow.QtWidgets.QMessageBox.warning")
    def test_email(self, mock_warn):
        result = self.window.create_new_user(
            "user", "pass", "no-at-sign", db_path=TEST_DB_PATH
        )
        self.assertEqual(result, "notValid")

    def tearDown(self):
        if QApplication.instance():
            QApplication.instance().quit()
        self.conn.close()
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)


# class TestAPI(unittest.TestCase):
"""
!API-TEST!
    def test_get_session(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '8bc7959e-153c-40dd-8da9-34e544661e71'
        }

        session = requests.Session()
        session.headers.update(headers)


        response = session.get(url)
        assert response.status_code == 200, "error not cnected"
        assert response.text == "OK"
"""


class TestBestenliste(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(testDB)
        self.c = self.conn.cursor()

        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                balance REAL DEFAULT 0
            )
        """
        )
        self.conn.commit()

        self.c.execute("DELETE FROM user WHERE username IN (?, ?)", ("marcel", "kiki"))
        self.conn.commit()

        self.c.execute(
            "INSERT INTO user (username, password, email, balance) VALUES (?, ?, ?, ?)",
            ("marcel", "pw", "m@gmail.com", 7200),
        )
        self.c.execute(
            "INSERT INTO user (username, password, email, balance) VALUES (?, ?, ?, ?)",
            ("kiki", "pw", "k@gmail.com", 5000),
        )
        self.conn.commit()
        self.conn.close()


class TestCryptoSearch(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(testDB)
        self.c = self.conn.cursor()

        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS coin (
                id INTEGER PRIMARY KEY,
                price FLOAT NOT NULL,
                name TEXT NOT NULL,
                supply INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                market_cap FLOAT NOT NULL,
                last_updated DATE NOT NULL
            )
        """
        )
        self.c.execute("DELETE FROM coin")
        self.conn.commit()

        self.c.execute(
            """
            INSERT INTO coin (id, price, name, supply, symbol, market_cap, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (1, 50000.0, "Bitcoin", 19000000, "BTC", 900000000000, "2024-06-10"),
        )
        self.conn.commit()

    def test_search_by_symbol(self):
        search_term = "BTC"
        self.c.execute("SELECT name FROM coin WHERE symbol = ?", (search_term,))
        result = self.c.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Bitcoin")

    def test_search_by_name(self):
        search_term = "Bitcoin"
        self.c.execute("SELECT symbol FROM coin WHERE name = ?", (search_term,))
        result = self.c.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "BTC")

    def tearDown(self):
        self.conn.close()


if __name__ == "__main__":
    unittest.main()
