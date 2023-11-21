import random
import string
from django.conf import settings
import requests


def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def send_sms_otp(phone_number, otp):
    # Mobizon API endpoint and API key
    api_key = "some_key"  # os.environ.get('API_KEY')
    api_url = f'https://api.mobizon.kz/service/Message/SendSmsMessage?apiKey={api_key}'

    # SMS message parameters
    recipient = str(phone_number)[1:]
    text = f'Код для активации аккаунта: {otp}'

    # Construct the request payload
    payload = {
        'recipient': recipient,
        'text': text,
    }

    # Make the API request
    # response = requests.post(api_url, data=payload)
    # print(response.json(), flush=True)
    print(payload, flush=True)
