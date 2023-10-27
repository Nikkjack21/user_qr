import uuid
import qrcode
import random
import string
from io import BytesIO
from django.core.files.base import ContentFile

BASE_SHORTEN_URL = "http://127.0.0.1:8000/api/accounts/"
SHORT_ID_LENGTH = 8


def generate_short_id():
    characters = string.ascii_letters + string.digits
    short_id = "".join(random.choice(characters) for _ in range(SHORT_ID_LENGTH))
    return short_id


def generate_short_url():
    token = generate_short_id()
    short_url = f"{BASE_SHORTEN_URL}{token}"
    return token, short_url


def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    unique_name = f"qr_code_{str(uuid.uuid4())[:8]}.png"
    image_file = ContentFile(img_buffer.getvalue(), name=unique_name)
    return image_file
