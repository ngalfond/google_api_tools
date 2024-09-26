import requests
import os
import statistics
import smtplib
from email.message import EmailMessage

#config = configparser.ConfigParser()
#config.read('.commute.conf')


url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
api_key = os.getenv('GOOGLE_API_KEY')
home_location = os.getenv('HOME_ADDRESS')
work_location = os.getenv('WORK_ADDRESS')
log_file = os.getenv('LOG_FILE')
contact = os.getenv('CONTACT')
snmp_server = os.getenv('SNMP_SERVER')
snmp_login = os.getenv('SNMP_LOGIN')

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
  if minutes!='0':
    return f"{minutes} minutes and {seconds} seconds"
  else:
     return f"{seconds} seconds"

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
       return(f"This is {make_readable(diff)} less than usual :)")
    if diff <= 0:
       diff = diff*(-1)
       return(f"This is {make_readable(diff)} more than usual :(")

def send_email(message):
  mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  mail_server.login(snmp_server, snmp_login)
  msg = EmailMessage()
  msg['From'] = "free.smtp.access@gmail.com"
  msg['To'] = contact
  msg.set_content(message)
  mail_server.send_message(msg)


       
#print(response.status_code)
response = requests.post(url, headers=headers, json=data)
trip_time = get_trip_time(response)
write_to_log(log_file, trip_time)
msg = (f'The current estimated commute to work will take {make_readable(trip_time)}.\n\n')
msg += find_difference(log_file)
print(msg)
send_email(msg)
