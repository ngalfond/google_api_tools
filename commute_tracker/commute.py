import googlemaps
import pprint
import statistics
import csv

gmaps = googlemaps.Client(key='AIzaSyDXr0gqy7jYfQG_aq20IHrbpu2zgxs3oaI')

work_location = 35.83158882391046, -82.67251414517058

home_location = 35.59424863065563, -82.55800273168425




full_matrix = gmaps.directions(home_location, work_location)

#pprint.pprint(full_matrix[0]["legs"][0]["duration"]["text"])

trip_time = (full_matrix[0]["legs"][0]["duration"]["text"])


print(f'The current estimated commute to work will take {trip_time}.')

time_int = int(trip_time.split()[0])

rev_matrix = gmaps.directions(work_location, home_location)

rev_time = (rev_matrix[0]["legs"][0]["duration"]["text"])

print(f'The trip back will take {rev_time}.')

with open('trips.csv', 'r+') as t:
    all_times = t.read().split(',')[:-1]
    t.write(f"{time_int},", )

int_times = map(int, all_times)

print(all_times)

print(statistics.mean(int_times))
