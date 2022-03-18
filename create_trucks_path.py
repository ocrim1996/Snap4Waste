import csv
import geopy.distance
from datetime import datetime
from build_map import build_map

input_filename = 'rest_mes_split_by_date/rest-2021-05-12.csv'
output_filename = 'trucks_paths.csv'
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
    if dst <= max_distance_allowed and diff <= 2700 and dst <= 1000:
        return True
    elif 2700 < diff < 4500 and dst <= 300:
        return True
    else:
        return False


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

    headers = ['id', 'lat', 'long', 'truck_num', 'date']
    with open(output_filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for index, path in enumerate(paths):
            for stop in path:
                row = [stop.id, stop.lat, stop.long, "truck"+str(index), stop.date]
                writer.writerow(row)

    print("Number of paths: "+str(len(paths)))
    build_map(output_filename)
