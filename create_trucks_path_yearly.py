import os
import csv
import geopy.distance
from datetime import datetime

# Iterate over directory.
directory = 'rest_mes_split_by_date'
filenames = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        filenames.append(f)
filenames = sorted(filenames)
filenames = filenames[:3]

output_filename = 'trucks_paths_yearly.csv'
speed_ms = 2.7777  # 10km/h in m/s
#speed_ms = 1.3888  # 5km/h in m/s


class Measure:
    def __init__(self, id, date, lat, long, weight):
        self.id = id
        self.lat = lat
        self.long = long
        self.date = date
        self.weight = weight

    def __str__(self):
        return self.id + " - " + str(self.date) + " - " + str(self.lat) + " - " + str(self.long) + " - " + str(
            self.weight)


def check_if_same_truck(measure1, measure2):
    # get distance between measures
    position1 = (measure1.lat, measure1.long)
    position2 = (measure2.lat, measure2.long)
    dst = geopy.distance.distance(position1, position2).km * 1000

    # get time between measures
    date1 = datetime.strptime(measure1.date, "%Y-%m-%dT%H:%M:%S.%fZ")
    date2 = datetime.strptime(measure2.date, "%Y-%m-%dT%H:%M:%S.%fZ")
    diff = (date1 - date2).seconds

    max_distance_allowed = diff * speed_ms
    # check if distance between bins is less than allowed distance and time diff less than 45 min
    if dst <= max_distance_allowed:
        return True
    else:
        return False


first_time = True
for input_filename in filenames:
    with open(input_filename, 'r') as myfile:
        reader = csv.reader(myfile)
        skip = next(reader, None)
        line = next(reader, None)
        first_mes = Measure(line[0], line[1], line[2], line[3], line[4])
        index_trucks = 0
        paths = [[]]
        paths[index_trucks].append(first_mes)
        for row in reader:
            measure = Measure(row[0], row[1], row[2], row[3], row[4])
            new_truck = True
            for path in paths:
                last_path_measure = path[-1]
                if check_if_same_truck(measure, last_path_measure):
                    path.append(measure)
                    new_truck = False
                    break
            if new_truck:
                index_trucks = index_trucks + 1
                paths.append([measure])

        headers = ['date', 'truck_num', 'weight']
        with open(output_filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            if first_time:
                writer.writerow(headers)
                first_time = False
            for index, path in enumerate(paths):
                for stop in path:
                    row = [stop.date[:-14], "truck"+str(index), stop.weight]
                    writer.writerow(row)

        print("Day" + str(input_filename.rsplit("/")[1][5:]) + ", Number of paths: "+str(len(paths)))
