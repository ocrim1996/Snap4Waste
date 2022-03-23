import os
import csv
from models import TruckPath as tp
from models import Measure as ms

# Iterate over directory.
directory = 'rest_mes_split_by_date'
filenames = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        filenames.append(f)
filenames = sorted(filenames)
# filenames = filenames[:3]

output_filename = 'trucks_paths_yearly.csv'

first_time = True
for input_filename in filenames:
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
                last_path_measure = path.measures[-1]
                if path.check_measure_in_path(measure):
                    path.add_measure(measure)
                    new_truck = False
                    break
            if new_truck:
                index_trucks = index_trucks + 1
                paths.append(tp.TruckPath(index_trucks))
                paths[index_trucks].add_measure(measure)

        headers = ['date', 'truck_num', 'weight']
        with open(output_filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            if first_time:
                writer.writerow(headers)
                first_time = False
            for index, path in enumerate(paths):
                for stop in path.measures:
                    row = [stop.date[:-14], "truck"+str(index), stop.weight]
                    writer.writerow(row)

        print("Day " + str(input_filename.rsplit("/")[1][5:]) + ", Number of paths: "+str(len(paths)))
