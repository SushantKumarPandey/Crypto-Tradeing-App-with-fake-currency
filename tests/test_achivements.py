def test_achievement_awarded_on_first_buy():
    fake_user = {"bought": 0}
    def buy_token(user):
        user["bought"] += 1
        if user["bought"] == 1:
            return "achievement awarded"
        return "no achievement"

    result = buy_token(fake_user)
    assert result == "achievement awarded"
