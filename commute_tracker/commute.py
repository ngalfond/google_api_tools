import requests
import os
import statistics

url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
api_key = os.getenv("GOOGLE_API_KEY")
home_location = os.getenv("HOME_ADDRESS")
work_location = os.getenv("WORK_ADDRESS")

log_file = "trips.csv"

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


def get_trip_time(req):
   trip_time_sec = int(req.json()['routes'][0]['duration'].replace("s", ""))
   trip_time = round((trip_time_sec/60), 2)
   return trip_time

def make_readable(time):
  minutes = str(time).split('.')[0]
  seconds = round(int(str(time).split('.')[1])*.6)
  return f"{minutes} minutes and {seconds} seconds"

def write_to_log(log, time):
  with open(log, 'a+') as t:
      t.write(f"{time},")

def calculate_average(log):
   with open(log, 'r') as t:
      all_times = t.read().split(',')[:-1]
      float_times = map(float, all_times)
      average_trip = round(statistics.mean(float_times), 2)
      return(average_trip)   
   
def find_difference(log):
    diff = round((calculate_average(log) - trip_time), 2)
    if diff > 0:
       print(f"This is {make_readable(diff)} less than usual :)")
    if diff <= 0:
       diff = diff*(-1)
       print(f"This is {make_readable(diff)} more than usual :(")
       
#print(response.status_code)

response = requests.post(url, headers=headers, json=data)
trip_time = get_trip_time(response)
write_to_log(log_file, trip_time)
print(f'The current estimated commute to work will take {make_readable(trip_time)}.')
find_difference(log_file)