import os
import pandas as pd
from sklearn.cluster import KMeans
from create_trucks_path_map import build_map
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

df = df.rename(columns={'dateObserved': 'date'})
df.to_csv(os.path.join(settings.csv_folder, "trucks_paths_kmeans.csv"), encoding='utf-8', index=False)

csv_file = os.path.join(settings.csv_folder, "trucks_paths_kmeans.csv")

build_map(csv_file, text)