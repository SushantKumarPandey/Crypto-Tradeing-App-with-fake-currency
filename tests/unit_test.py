import unittest

def login(username, password):
    return username == "user" and password == "pass123"

registered_users = []

def register(username, password):
    if username in registered_users:
        return False
    registered_users.append(username)
    return True


def test_successful_login():
    assert login("user", "pass123") == True

def test_failed_login_wrong_password():
    assert login("user", "wrongpass") == False

def test_failed_login_unknown_user():
    assert login("unknown", "pass123") == False

def test_successful_registration():
    registered_users.clear()  # reset user list before test
    result = register("newuser", "securepassword")
    assert result == True
    assert "newuser" in registered_users

def test_duplicate_registration():
    registered_users.clear()
    register("newuser", "securepassword")
    result = register("newuser", "anotherpass")
    assert result == False

def test_fake_balance():
    fake_balance = 1000
    assert fake_balance >= 0


    def test_achievement_awarded_on_first_buy(self):
        fake_user = {"bought": 0}
        result = buy_token(fake_user)
        self.assertEqual(result, "achievement awarded")


if __name__ == "__main__":
    unittest.main()




