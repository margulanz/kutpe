import random
import string
import requests
import math
import joblib
import numpy as np
from django.conf import settings
import datetime


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
    # print(payload, flush=True)


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


WeekDay_business = {
    'Monday': [30, 10, 7],
    'Tuesday': [30, 10, 7]
}


def datetime_to_features(dt):
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    day_of_week = dt.weekday()
    day_of_week_binary = [0] * 7
    day_of_week_binary[day_of_week] = 1
    return [hour, minute] + day_of_week_binary


def arrival_interval_time():
    now = datetime.datetime.now()
    data = datetime_to_features(now)
    model = joblib.load('finalized_model.pkl')
    features = np.array([data])
    predicted_arrivals = model.predict(features)
    return predicted_arrivals[0]


def calculate_time(num_servers=2, max_service=20, min_service=10):
    lambdaa = 1/arrival_interval_time()
    mean_service_time = (min_service + max_service)/2
    mewing = 1/mean_service_time
    variance_s = pow(max_service-min_service, 2)/12
    p = lambdaa/(num_servers*mewing)
    C_s = variance_s/pow(mean_service_time, 2)
    sum = 0
    for i in range(num_servers-1):
        sum += pow(num_servers*p, i)/math.factorial(i)
    sum += pow(num_servers*p, num_servers) / \
        (math.factorial(num_servers)*(1 - p))
    p_0 = 1/sum
    L_q = p_0*pow(lambdaa/mewing, num_servers)*p / \
        (math.factorial(num_servers)*pow(1-p, 2))
    W_q = L_q/lambdaa
    return (L_q, W_q)
