import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import plotly.express as px
import csv
from settings import settings


df = pd.read_csv(os.path.join(settings.csv_ams_api_folder, "ams-rest-2021-12-28.csv"))


kmeans = KMeans(n_clusters=30, init='k-means++')
kmeans.fit(df[df.columns[2:4]]) # Compute k-means clustering.
df['truck_num'] = kmeans.fit_predict(df[df.columns[2:4]])
centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
labels = kmeans.predict(df[df.columns[2:4]]) # Labels of each point

df = df.sort_values(by=['truck_num', 'dateObserved'])
df['truck_num'] = 'truck' + df['truck_num'].astype(str)

first_truck = df['truck_num'].iloc[0]
sum_weight = []
last_measure = 0
text = "<b>Trucks</b> &nbsp; <b>Tot_Weights</b><br>"
for idx, truck in enumerate(df['truck_num']):
    if truck == first_truck:
        measure = df['weight'].iloc[idx] + last_measure
        sum_weight.append(measure)
        last_measure = measure
    else:
        first_truck = truck
        measure = df['weight'].iloc[idx]
        sum_weight.append(measure)
        last_measure = measure

df['sum_weight'] = sum_weight


maximum_weights = df.groupby('truck_num', sort=False)['sum_weight'].max().reset_index()
trucks = maximum_weights['truck_num'].values
sums = maximum_weights['sum_weight'].values
for i in range(len(trucks)):
    text = text + str(trucks[i]) + " -> " + str(sums[i]) + " Kg<br>"


df.to_csv(os.path.join(settings.csv_folder, "trucks_paths_kmeans.csv"), encoding='utf-8', index=False)

csv_file = os.path.join(settings.csv_folder, "trucks_paths_kmeans.csv")
container_pos = pd.read_csv(csv_file)


legend_dict = dict(
        x=0,
        y=1,
        title_font_family="Times New Roman",
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),
        bgcolor="#f0f3ef",
        bordercolor="Black",
        borderwidth=2
    )

fig = px.line_mapbox(container_pos, lat="lat", lon="long", hover_name="sum_weight", text="dateObserved", color="truck_num", zoom=3)

fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=11, mapbox_center_lat=52.370579,
                      mapbox_center_lon=4.902242, legend=legend_dict, margin={"r":0,"t":0,"l":0,"b":0})

fig.add_annotation(
    text=text,
    xref="paper",
    yref="paper",
    align="left",
    x=0.99,
    y=0.98,
    showarrow=False,
    font=dict(
        family="Courier",
        size=10,
        color="black"
    ),
    bgcolor="#f0f3ef",
    bordercolor="Black",
    borderwidth=2
)

fig.show()