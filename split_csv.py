import os
from datetime import datetime
import csv
from settings import settings

input_file = os.path.join(settings.csv_folder, 'rest_measures_with_pos_by_date.csv')

with open(input_file, 'r') as myfile:
    reader = csv.reader(myfile)
    skip = next(reader, None)
    #line = next(reader, None)
    date = "2020-01-01"
    headers = ['id', 'dateObserved', 'lat', 'long', 'weight', 'day_diff']

    count = 0
    for row in reader:
        date_to_check = str(datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ").date())
        output_filename = os.path.join(settings.csv_mes_disit_folder, 'rest-' + date_to_check + '.csv')

        with open(output_filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            if count == 0:
                writer.writerow(headers)

            if date_to_check == date:
                count = count + 1
                writer.writerow(row)
            else:
                writer.writerow(headers)
                date = date_to_check
                writer.writerow(row)





