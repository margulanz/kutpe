import random
import string
import requests
import math
import joblib
import numpy as np
from django.conf import settings
import datetime
import google.generativeai as genai
import os

API_KEY = "AIzaSyBO4vStpGCCBkxFDTiUy9zPOFdXkmK_cjc"


def generate_response():
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    time = datetime.datetime.now()
    minute = time.minute
    rounded_minutes = minute // 10 * 10
    hour = time.hour

    original_time = f"{hour:02d}:{time.minute:02d}"
    rounded_time = f"{hour:02d}:{rounded_minutes:02d}"

    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(script_dir, "input.txt")

    with open(input_file_path, "r") as file:
        text = file.read()

    text = (
        text
        + f"Given the dataset's information about arrivals in 10-minute intervals, the current time is {original_time}, corresponding to the data point closest to {rounded_time}. Please advise whether visiting the place is recommended based on its arrival rate at this time. Keep the response short and informative, focusing on whether it's overcrowded or not. For example, you might say, 'It's overcrowded right now,' or 'It's not too crowded at the moment.'"
    )

    response = model.generate_content(text)

    return response.text


def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_sms_otp(phone_number, otp):
    # Mobizon API endpoint and API key
    api_key = "some_key"  # os.environ.get('API_KEY')
    api_url = f"https://api.mobizon.kz/service/Message/SendSmsMessage?apiKey={api_key}"

    # SMS message parameters
    recipient = str(phone_number)[1:]
    text = f"Код для активации аккаунта: {otp}"

    # Construct the request payload
    payload = {
        "recipient": recipient,
        "text": text,
    }

    # Make the API request
    # response = requests.post(api_url, data=payload)
    # print(response.json(), flush=True)
    # print(payload, flush=True)


def get_location_coordinates(location_str):
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {"format": "json", "q": location_str}

    response = requests.get(nominatim_url, params=params)
    data = response.json()

    if data and len(data) > 0:
        location = data[0]
        return f"{location['lat']},{location['lon']}"
    else:
        return None


def find_nearest_banks(location, radius=1500, amenity="bank"):
    # location = get_location_coordinates(location_str)

    if location:
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
            [out:json];
            node(around:{radius},{location})["amenity"="{amenity}"];
            out;
        """

        response = requests.post(overpass_url, data=overpass_query)
        data = response.json().get("elements", [])

        return data
    else:
        print("Invalid location.")


def find_nearest_banks_by_location(location_str, radius=1500, amenity="bank"):
    location = get_location_coordinates(location_str)

    if location:
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
            [out:json];
            node(around:{radius},{location})["amenity"="{amenity}"];
            out;
        """

        response = requests.post(overpass_url, data=overpass_query)
        data = response.json().get("elements", [])

        return data
    else:
        print("Invalid location.")


WeekDay_business = {"Monday": [30, 10, 7], "Tuesday": [30, 10, 7]}


def datetime_to_features(dt):
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    day_of_week = dt.weekday()
    day_of_week_binary = [0] * 7
    day_of_week_binary[day_of_week] = 1
    return [hour, minute] + day_of_week_binary


def arrival_interval_time(time):
    # now = datetime.datetime.now()
    data = datetime_to_features(time)
    model = joblib.load("backend/finalized_model.pkl")
    features = np.array([data])
    print(features, flush=True)
    predicted_arrivals = model.predict(features)
    return predicted_arrivals[0]


def calculate_time(time, num_servers=2, max_service=20, min_service=10):
    # now = datetime.datetime.now()
    lambdaa = 1 / arrival_interval_time(time)
    mean_service_time = (min_service + max_service) / 2
    mewing = 1 / mean_service_time
    variance_s = pow(max_service - min_service, 2) / 12
    p = lambdaa / (num_servers * mewing)
    C_s = variance_s / pow(mean_service_time, 2)
    sum = 0
    for i in range(num_servers - 1):
        sum += pow(num_servers * p, i) / math.factorial(i)
    sum += pow(num_servers * p, num_servers) / (math.factorial(num_servers) * (1 - p))
    p_0 = 1 / sum
    L_q = (
        p_0
        * pow(lambdaa / mewing, num_servers)
        * p
        / (math.factorial(num_servers) * pow(1 - p, 2))
    )
    W_q = L_q / lambdaa
    return (L_q, W_q)
