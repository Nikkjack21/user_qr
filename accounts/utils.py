import random
import string


BASE_SHORTEN_URL = "http://127.0.0.1:8000/"
SHORT_ID_LENGTH = 8


def generate_short_id():
    characters = string.ascii_letters + string.digits
    short_id = "".join(random.choice(characters) for _ in range(SHORT_ID_LENGTH))
    return short_id


def generate_short_url():
    short_id = generate_short_id()
    short_url = f"{BASE_SHORTEN_URL}{short_id}"
    return short_url


def generate_qr_code(data):
    pass
