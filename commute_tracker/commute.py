import requests
import os
import statistics

url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
api_key = os.getenv("GOOGLE_API_KEY")
home_location = os.getenv("HOME_ADDRESS")
work_location = os.getenv("WORK_ADDRESS")

headers = {'Content-Type': 'application/json',
           'X-Goog-Api-Key': api_key,
           'X-Goog-FieldMask': 'routes.duration'}

data = {
  "origin":{
    "address": home_location
  },
  "destination":{
    "address": work_location
  },
  "travelMode": "DRIVE",
  "routingPreference": "TRAFFIC_AWARE",
  "computeAlternativeRoutes": False,
  "languageCode": "en-US",}

response = requests.post(url, headers=headers, json=data)
print(response.json())
trip_time_sec = int(response.json()['routes'][0]['duration'].replace("s", ""))

trip_time = round((trip_time_sec/60), 2)

print(response.status_code)
print(trip_time)


with open('trips.csv', 'r+') as t:
    all_times = t.read().split(',')[:-1]
    t.write(f"{trip_time},", )

float_times = map(float, all_times)

print(all_times)

average_trip = round(statistics.mean(float_times), 2)
print(average_trip)

minutes = str(trip_time).split('.')[0]
seconds = round(int(str(trip_time).split('.')[1])*.6)
print(f'The current estimated commute to work will take {minutes} minutes and {seconds} seconds.')
