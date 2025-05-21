import sqlite3
import unittest


class TestDB(unittest.TestCase):

    def test_connected(self):
        try:
            conn = sqlite3.connect('../client/crypto.db')
            c = conn.cursor()
            state="Conected"
            conn.close()
        except:
            state="Disconnected"
        self.assertEqual(state, "Conected")


    def test_getAllUsers(self):
        conn = sqlite3.connect('../client/crypto.db')
        c = conn.cursor()
        c.execute("SELECT username FROM user WHERE id < 3")
        users = [row[0] for row in c.fetchall()]
        expectedNames = ["kiki", "marcel"]
        self.assertEqual(users, expectedNames)

        conn.close()

    def test_password_fromUser(self):
        conn = sqlite3.connect('../client/crypto.db')
        c = conn.cursor()
        c.execute("SELECT password FROM user WHERE username = 'kiki' ")
        password = c.fetchone()[0]
        self.assertEqual(password, 'quack')

        conn.close()

    def test_email_fromUser(self):
        conn = sqlite3.connect('../client/crypto.db')
        c = conn.cursor()
        c.execute("SELECT email FROM user WHERE username = 'kiki' ")
        password = c.fetchone()[0]
        self.assertEqual(password, 'bsp1@gmail.com')

        conn.close()


if __name__ == '__main__':
    unittest.main()