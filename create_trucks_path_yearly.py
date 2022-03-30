import os
import csv
from models import TrucksPathScore as tps
from models import Measure as ms
from settings import settings

# Iterate over directory.
#directory = settings.csv_mes_disit_folder
directory = settings.csv_ams_api_folder
filenames = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        filenames.append(f)
filenames = sorted(filenames)

output_filename = os.path.join(settings.csv_folder, 'ams_trucks_paths_yearly_16000_3000.csv')

first_time = True
for input_filename in filenames:
    with open(input_filename, 'r') as myfile:
        reader = csv.reader(myfile)
        skip = next(reader, None)
        line = next(reader, None)
        first_mes = ms.Measure(line[0], line[1], line[2], line[3], line[4])
        index_trucks = 0
        paths = [tps.TruckPath(index_trucks)]
        paths[index_trucks].add_measure(first_mes)
        for row in reader:
            #print(row[1])
            measure = ms.Measure(row[0], row[1], row[2], row[3], row[4])
            new_truck = True
            best_index = None
            best_score = None
            for index, path in enumerate(paths):
                result = path.check_measure_in_path(measure)
                if result[0]:
                    if best_score is None or result[1] < best_score:
                        new_truck = False
                        best_index = index
                        best_score = result[1]
            if new_truck is False:
                paths[best_index].add_measure(measure)
            else:
                index_trucks = index_trucks + 1
                paths.append(tps.TruckPath(index_trucks))
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
