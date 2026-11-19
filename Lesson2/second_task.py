MIN_PASSWORD_LENGTH = 8


def validate_user(username, password, age):
    is_password_long_enough = len(password) >= MIN_PASSWORD_LENGTH
    is_adult = age >= 18

    return is_password_long_enough and is_adult
