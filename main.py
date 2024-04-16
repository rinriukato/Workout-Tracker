import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Constant Data
API_ID = os.getenv('NT_API_ID')
API_KEY = os.getenv('NT_API_KEY')
GENDER = # YOUR GENDER
WEIGHT_KG =  # YOUR WEIGHT
HEIGHT_CM = # YOUR HEIGHT
AGE = # YOUR AGE

nutr_endpoint = os.getenv('NT_ENDPOINT')
sheety_endpoint = os.getenv('SHEETY_ENDPOINT')
token = os.getenv('SHEETY_TOKEN')

# Ask User for input
query = input("Tell me which exercise you did: ")

header = {
    'x-app-id': API_ID,
    'x-app-key': API_KEY,
}

param = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

# API Request to nutritionix to get calories calculations
response = requests.post(url=nutr_endpoint, json=param, headers=header)
response.raise_for_status()
data = response.json()['exercises']


# Post to Sheety and Update connected Google Sheet.
today = datetime.now()
current_date = today.strftime("%d/%m/%Y")
current_time = today.strftime("%X")

sheety_header = {
    "Authorization": f"Bearer {token}"
}

for exercise in data:
    new_workout = {
        "workout": {
            "date": current_date,
            "time": current_time,
            "exercise": exercise['user_input'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }

    response = requests.post(url=sheety_endpoint, json=new_workout, headers=sheety_header)
    response.raise_for_status()
