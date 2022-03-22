import csv
import geopy.distance
from datetime import datetime
from build_map import build_map

input_filename = 'rest_mes_split_by_date/rest-2021-12-30.csv'
output_filename = 'trucks_paths.csv'
speed_ms = 4  # 10km/h in m/s
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


class TruckPath:
    def __init__(self, index):
        self.index = index
        self.centroid_latitude = 0
        self.centroid_longitude = 0
        self.measures = []

    def add_measure(self, new_measure):
        self.measures.append(new_measure)
        self.update_centroid()

    def update_centroid(self):
        lat_centroid = 0
        long_centroid = 0
        n_measures = len(self.measures)
        for measure in self.measures:
            lat_centroid = lat_centroid + float(measure.lat)
            long_centroid = long_centroid + float(measure.long)
        lat_centroid = lat_centroid/n_measures
        long_centroid = long_centroid/n_measures
        self.centroid_latitude = lat_centroid
        self.centroid_longitude = long_centroid

    def check_measure_in_path(self, measure):
        # get distance between measures
        position1 = (self.centroid_latitude, self.centroid_longitude)
        position2 = (measure.lat, measure.long)
        dst = geopy.distance.distance(position1, position2).km * 1000

        # get time between measures
        #print("Ultima: "+self.measures[-1].date)
        date1 = datetime.strptime(self.measures[-1].date, "%Y-%m-%dT%H:%M:%S.%fZ")
        date2 = datetime.strptime(measure.date, "%Y-%m-%dT%H:%M:%S.%fZ")
        #print("d1: "+str(date1)+" - d2: "+str(date2))
        diff = (date2 - date1).seconds

        max_distance_allowed = diff * speed_ms
        # check if distance between bins is less than allowed distance and time diff less than 45 min
        print(str(dst)+" controllo "+str(max_distance_allowed))
        if dst <= max_distance_allowed and dst < 3000:
            return True
        else:
            return False


with open(input_filename, 'r') as myfile:
    reader = csv.reader(myfile)
    skip = next(reader, None)
    line = next(reader, None)
    first_mes = Measure(line[0], line[1], line[2], line[3], line[4])
    index_trucks = 0
    paths = [TruckPath(index_trucks)]
    paths[index_trucks].add_measure(first_mes)
    for row in reader:
        print(row[1])
        measure = Measure(row[0], row[1], row[2], row[3], row[4])
        new_truck = True
        for path in paths:
            if path.check_measure_in_path(measure):
                path.add_measure(measure)
                new_truck = False
                break
        if new_truck:
            index_trucks = index_trucks + 1
            paths.append(TruckPath(index_trucks))
            paths[index_trucks].add_measure(first_mes)
        print("------------")

    headers = ['id', 'lat', 'long', 'truck_num', 'date', 'weight']
    with open(output_filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for index, path in enumerate(paths):
            for stop in path.measures:
                row = [stop.id, stop.lat, stop.long, "truck"+str(index), stop.date, stop.weight]
                writer.writerow(row)

    print("Number of paths: "+str(len(paths)))
    build_map(output_filename)
