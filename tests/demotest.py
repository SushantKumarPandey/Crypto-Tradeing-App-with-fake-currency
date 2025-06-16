import sys
import sqlite3
import unittest
sys.path.insert(0, '../client')
from client.mainwindow import Registerwindow
from werkzeug.security import check_password_hash
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)  # Einmalig vor allen Tests, z.B. ganz oben in der Datei


testDB = "../client/crypto.db"

class TestDB(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(testDB)
        self.c = self.conn.cursor()

        self.c.execute('''
         CREATE TABLE IF NOT EXISTS user(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT UNIQUE NOT NULL,
         password TEXT NOT NULL,
         email TEXT NOT NULL
         )
     ''')
        self.c.execute('DELETE FROM user WHERE username = ?', ("tester",))
        self.c.execute('INSERT INTO user (username, password, email) VALUES (?, ?, ?)',
                  ("tester", "password", "bsp@email.com"))

        self.conn.commit()
        self.conn.close()

    def test_connected(self):
        try:
            conn = sqlite3.connect(testDB)
            c = conn.cursor()
            state = "Conected"
            conn.close()
        except:
            state = "Disconnected"
        self.assertEqual(state, "Conected")

    def test_getUsers(self):
        conn = sqlite3.connect(testDB)
        c = conn.cursor()

        c.execute("SELECT username FROM user WHERE username =  ?", ("tester",))
        user =c.fetchone()
        conn.close()
        assert(user is not None)
        assert(user[0] == "tester")

    def test_password_fromUser(self):
        conn = sqlite3.connect('../client/crypto.db')
        c = conn.cursor()
        c.execute("SELECT password FROM user WHERE username = 'kiki' ")
        password = c.fetchone()[0]
        self.assertEqual(password, 'quack')

        conn.close()

    def test_hasedPassword(self):
        conn = sqlite3.connect('../client/crypto.db')
        c = conn.cursor()
        c.execute("SELECT password FROM user WHERE username = 'safe' ")
        hashed_password = c.fetchone()[0]
        password = "safe"

        self.assertNotEqual(hashed_password, 'safe')
        self.assertTrue(check_password_hash(hashed_password, password))
        conn.close()

    def test_email_fromUser(self):
        conn = sqlite3.connect('../client/crypto.db')
        c = conn.cursor()
        c.execute("SELECT email FROM user WHERE username = 'kiki' ")
        email = c.fetchone()[0]
        self.assertEqual(email, 'bsp1@gmail.com')

        conn.close()

class TestHTTP(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(testDB)
        self.c = self.conn.cursor()

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
            )
        ''')
        self.c.execute('DELETE FROM user WHERE username = ?', ("tee",))
        self.c.execute('DELETE FROM user WHERE username = ?', ("user",))
        self.conn.commit()
        self.conn.close()
        self.window=Registerwindow()

    def test_createUser(self):
        new_user = self.window.create_new_user("tee", "secure", "email@example.com")
        self.assertEqual(new_user, "success")

    def test_usernameUnique(self):
        conn = sqlite3.connect(testDB)
        c = conn.cursor()
        try:
            self.c.execute('INSERT INTO user (username, password, email) VALUES (?, ?, ?)',
                  ("tester", "password", "bsp@email.com"))
            message="new accouont"
        except:
            message="name already taken"
        conn.close()
        self.assertEqual(message, "name already taken")

    def test_email(self):
        result = self.window.create_new_user('user', 'pass', 'no-at-sign')
        self.assertEqual(result, 'notValid')

    def test(self):
        pass

# class TestAPI(unittest.TestCase):
'''
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
'''



if __name__ == '__main__':
    unittest.main()
