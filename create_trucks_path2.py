import os
import csv
from models import TruckPath as tp
from models import Measure as ms
from create_trucks_path_map import build_map
from settings import settings

input_filename = os.path.join(settings.csv_ams_api_folder, 'ams-rest-2021-03-23.csv')
output_filename = os.path.join(settings.csv_folder, 'trucks_paths.csv')


with open(input_filename, 'r') as myfile:
    reader = csv.reader(myfile)
    skip = next(reader, None)
    line = next(reader, None)
    first_mes = ms.Measure(line[0], line[1], line[2], line[3], line[4])
    index_trucks = 0
    paths = [tp.TruckPath(index_trucks)]
    paths[index_trucks].add_measure(first_mes)
    for row in reader:
        measure = ms.Measure(row[0], row[1], row[2], row[3], row[4])
        new_truck = True
        for path in paths:
            if path.check_measure_in_path(measure):
                path.add_measure(measure)
                new_truck = False
                break
        if new_truck:
            index_trucks = index_trucks + 1
            paths.append(tp.TruckPath(index_trucks))
            paths[index_trucks].add_measure(measure)

    headers = ['id', 'lat', 'long', 'truck_num', 'date', 'weight', 'sum_weight']
    with open(output_filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        text = "<b>Trucks</b> &nbsp; <b>Tot_Weights</b><br>"
        for index, path in enumerate(paths):
            sum = 0
            for stop in path.measures:
                sum = sum + stop.weight
                row = [stop.id, stop.lat, stop.long, "truck"+str(index), stop.date, stop.weight, sum]
                writer.writerow(row)
            print("weight path: " + str(path.index) + " = " + str(sum))
            text = text + "truck" + str(path.index) + " -> " + str(sum) + " Kg<br>"

    print("Number of paths: "+str(len(paths)))
    build_map(output_filename, text)
