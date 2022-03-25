import os
import requests
from rijksdriehoek import rijksdriehoek
import pandas as pd
import csv
from settings import settings


def convert_to_wgs84(x, y):
    rd = rijksdriehoek.Rijksdriehoek(x, y)
    lat, long = rd.to_wgs()
    return lat, long


days = pd.date_range(start="2021-09-28", end="2021-12-31")
for i in days:
    date = str(i.date())
    print(date)

    output_filename = os.path.join(settings.csv_ams_api_folder, "ams-rest-" + date + ".csv")

    response = requests.get("https://api.data.amsterdam.nl/v1/huishoudelijkafval/weging/?datumWeging=" + date +
                       "&fractieOmschrijving=Rest&clusterId[isnull]=false&nettoGewicht["
                       "isnull]=false&_format=json&_pageSize=5000").json()

    if len(response["_embedded"]["weging"]) > 0:
        headers = ['id', 'dateObserved', 'lat', 'long', 'weight']
        with open(output_filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for elem in response["_embedded"]["weging"]:
                id = elem["clusterId"].replace("|", "_") + "-Rest"
                dateObserved = elem["datumWeging"] + "T" + elem["tijdstipWeging"] + ".000Z"
                coordinates = elem["geometrie"]["coordinates"]
                lat, long = convert_to_wgs84(coordinates[0], coordinates[1])
                weight = elem["nettoGewicht"]
                row = [id, dateObserved, lat, long, weight]
                writer.writerow(row)



