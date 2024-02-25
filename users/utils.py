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


def get_location_coordinates(location_str):
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'format': 'json',
        'q': location_str
    }

    response = requests.get(nominatim_url, params=params)
    data = response.json()

    if data and len(data) > 0:
        location = data[0]
        return f"{location['lat']},{location['lon']}"
    else:
        return None


def find_nearest_banks(location, radius=1500, amenity='bank'):
    # location = get_location_coordinates(location_str)

    if location:
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
            [out:json];
            node(around:{radius},{location})["amenity"="{amenity}"];
            out;
        """

        response = requests.post(overpass_url, data=overpass_query)
        data = response.json().get('elements', [])

        return data
    else:
        print("Invalid location.")


def find_nearest_banks_by_location(location_str, radius=1500, amenity='bank'):
    location = get_location_coordinates(location_str)

    if location:
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
            [out:json];
            node(around:{radius},{location})["amenity"="{amenity}"];
            out;
        """

        response = requests.post(overpass_url, data=overpass_query)
        data = response.json().get('elements', [])

        return data
    else:
        print("Invalid location.")
