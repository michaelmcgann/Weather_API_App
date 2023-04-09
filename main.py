import requests
import pandas as pd
from twilio.rest import Client


def test_for_condition(condition_1):
    if condition_1 == 'Clouds':
        emoji = '☁️'

    elif condition_1 == 'Clear':
        emoji = '☀️'

    elif condition_1 == 'Fog':
        emoji = '🌫️'

    elif condition_1 == 'Snow':
        emoji = '🌨️'

    elif condition_1 == 'Rain' or condition_1 == 'Drizzle':
        emoji = '🌧️'

    elif condition_1 == 'Thunderstorm':
        emoji = '🌩️'

    else:
        emoji = ''

    return emoji


api_key = '<PUT API HERE>'
lat = 53.8008
lon = -1.5491
url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'

account_sid = 'AC944c3e43cf0bd798216f96028dc211a2'
auth_token = '<PUT AUTH TOKEN HERE>'
client = Client(account_sid, auth_token)


response = requests.get(url=url)
response.raise_for_status()

data = response.json()

time_list = []
condition_list = []
description_list = []


for section in data['list']:
    time = section['dt_txt']
    condition = section['weather'][0]['main']
    description = section['weather'][0]['description']
    weather_id = section['weather'][0]['id']

    time_list.append(time)
    condition_list.append(condition)
    description_list.append(description)


weather_dt = pd.DataFrame({'Time': time_list, 'Condition': condition_list, 'Description': description_list})
print(weather_dt)

text = '\n'
for index, row in weather_dt.head(5).iterrows():
    hour_time = row['Time'][11:]

    condition_2 = row['Condition']
    emoji = test_for_condition(condition_2)

    text += f"{row['Description']} at {hour_time} {emoji}\n"

print(text)
client = Client(account_sid, auth_token)
message = client.messages \
    .create(
        body=f"{text}",
        from_='<PUT TWILIO NUMBER HERE>',
        to='<PUT YOUR NUMBER HERE>'
        )



