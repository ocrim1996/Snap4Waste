import folium
from folium import plugins
import csv

m = folium.Map(location=[52.370579, 4.902242], tiles="CartoDB Positron", zoom_start=12)

input_filename = 'rest_mes_split_by_date/rest-2021-05-12.csv'

points = []

with open(input_filename, 'r') as myfile:
    reader = csv.reader(myfile)
    skip = next(reader, None)
    for row in reader:
        coordinates = [float(row[3]), float(row[2])]
        date = row[1][:-5]
        if float(row[4]) <= 1500:
            color = "blue"
        else:
            color = "red"

        point_json = {
            "coordinates": coordinates,
            "dates": date,
            "color": color,
        },
        points.append(point_json[0])

features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"],
        },
        "properties": {
            "time": point["dates"],
            "style": {
                "color": point["color"],
            },
            "icon": "circle",
            "iconstyle": {
                "fillColor": point["color"],
                "stroke": "true",
                "radius": 5,
            }
        },
    }
    for point in points
]


plugins.TimestampedGeoJson(
    {
        "type": "FeatureCollection",
        "features": features,
    },
    period="PT1M",
    add_last_point=True,
).add_to(m)

m.save('index.html')
