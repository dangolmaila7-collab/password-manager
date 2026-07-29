"""Generates strong random passwords that always contain at least
one uppercase letter, one lowercase letter, one digit and one symbol.
"""
import random
import string


def generate_password(length=12):
    digits = string.digits
    symbols = "!@#$%^&*"
    pool = string.ascii_letters + digits + symbols

    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(digits),
        random.choice(symbols),
    ]
    while len(password) < length:
        password.append(random.choice(pool))

    random.shuffle(password)
    return "".join(password)