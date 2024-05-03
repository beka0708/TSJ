import logging
import random
import string

import requests
from decouple import config

logger = logging.getLogger(__name__)


def generate_verification_code(length=4):
    """
    Генерирует случайный код подтверждения указанной длины.
    """
    characters = string.digits
    verification_code = ''.join(random.choice(characters) for _ in range(length))
    return verification_code


def send_verification_sms(phone_number):
    """
    Отправляет SMS с этим кодом на указанный номер телефона.
    """
    verification_code = generate_verification_code(length=4)
    api_key = config("API_KEY")
    secret_key = config("SECRET_KEY_SMS")
    sms_text = f"Ваш код для подтверждения: {verification_code}"
    url = "https://api.smspro.nikita.kg/send"
    payload = {
        "api_key": api_key,
        "secret_key": secret_key,
        "phone": phone_number,
        "text": sms_text
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error sending verification SMS: {e}")
        return None

    if response.status_code == 200:
        logger.info("Verification SMS sent successfully")
        return verification_code
    else:
        logger.error("Error sending verification SMS")
        return None
