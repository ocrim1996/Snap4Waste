import csv
import numpy as np
import os
from settings import settings

input_filename = os.path.join(settings.csv_folder, 'ams_id_list_rest_sorted.csv')
output_filename = os.path.join(settings.csv_folder, 'ams_id_list_rest_stats.csv')

with open(input_filename, 'r') as myfile:
    reader = csv.reader(myfile)
    line = next(reader, None)

    headers = ['id', 'lat', 'long', 'avg_weight', 'container_type', 'num_weights']
    with open(output_filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        w_array = []

        line = next(reader, None)
        id = line[0]
        w_array.append(float(line[4]))

        for row in reader:
            if row[0] == id:
                w_array.append(float(row[4]))
            else:
                lat = row[2]
                long = row[3]
                np_w_array = np.asarray(w_array)

                w_avg = np.round(np.mean(np_w_array), decimals=1)
                num_weights = len(np_w_array)

                if w_avg <= 1500:
                    container_type = "Normal container"
                else:
                    container_type = "Big container"

                stats_row = [id, lat, long, w_avg, container_type, num_weights]
                writer.writerow(stats_row)
                id = row[0]

                w_array = []
                w_array.append(float(row[4]))