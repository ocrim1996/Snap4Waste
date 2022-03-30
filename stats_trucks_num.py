import os
import pandas as pd
import numpy as np
import collections
from statistics import mean, median
from settings import settings

file1 = pd.read_csv(os.path.join(settings.csv_folder, "ams_trucks_num_16000_4000.csv"))

trucks_num = file1.tot_trucks.to_list()

trucks_mean = mean(trucks_num)
trucks_median = median(trucks_num)

print("Numero medio di camion:", trucks_mean)
print("Numero mediano di camion:", trucks_median)
print("*"*50)

file2 = pd.read_csv(os.path.join(settings.csv_folder, "ams_trucks_load_yearly_16000_4000.csv"))

load = file2.tot_weight.to_list()

load_mean = mean(load)
load_median = median(load)

print("Peso medio fine giro:", load_mean)
print("Peso mediano fine giro:", load_median)
print("*"*50)

trucks_load = pd.read_csv(os.path.join(settings.csv_folder, "ams_trucks_paths_yearly_16000_4000.csv"))

trucks_load['tot_weight'] = trucks_load.groupby(['date', 'truck_num'])['weight'].transform('sum')
trucks_load = trucks_load.drop_duplicates(subset=['date', 'truck_num'], keep='last')
trucks_load = trucks_load[['date', 'truck_num', 'tot_weight']]

def percentage(part, whole):
  percentage = round(100 * float(part)/float(whole), 2)
  return str(percentage) + "%"

df = trucks_load
n_camions = len(trucks_load['tot_weight'])
print(df.describe(percentiles=[.25, .5, .75, .99]))

n_camion_carichi = len(df[df['tot_weight'] >= 12000])
print("\nNumero di camion carichi (peso ≥ 12000): " + str(n_camion_carichi) + ", Percentuale: " + str(percentage(n_camion_carichi, n_camions)))

n_camion_semi_carichi = len(df[(df['tot_weight'] < 12000) & (df['tot_weight'] >= 8000)])
print("Numero di camion semi-carichi (8000 ≤ peso < 12000): " + str(n_camion_semi_carichi) + ", Percentuale: " + str(percentage(n_camion_semi_carichi, n_camions)))

n_camion_semi_vuoti = len(df[(df['tot_weight'] < 8000) & (df['tot_weight'] >= 4000)])
print("Numero di camion semi-vuoti (4000 ≤ peso < 8000): " + str(n_camion_semi_vuoti) + ", Percentuale: " + str(percentage(n_camion_semi_vuoti, n_camions)))

n_camion_vuoti = len(df[df['tot_weight'] < 4000])
print("Numero di camion vuoti (peso < 4000): " + str(n_camion_vuoti) + ", Percentuale: " + str(percentage(n_camion_vuoti, n_camions)))
print("*"*50)


# Python program to count the frequency of
# elements in a list using a dictionary

def CountFrequency(my_list):
    # Creating an empty dictionary
    freq = {}
    for items in my_list:
        freq[items] = my_list.count(items)

    my_dict = {}
    for key, value in freq.items():
        #print("% d : % d" % (key, value))
        my_dict[key] = value
    my_dict_items = my_dict.items()
    sorted_items = sorted(my_dict_items)

    sorted_items = dict(sorted_items)
    sorted_items.pop(-120.0)
    return sorted_items

my_list = load
a = CountFrequency(my_list)

measures = []
avg_weights = []
for key, value in a.items():
    #print("Key:" +str(key) +", Value:" + str(value))
    measures.append(key)
    avg_weights.append(value)

measures_np = np.asarray(measures)
avg_weights_np = np.asarray(avg_weights)

media_pesata = np.average(measures_np, weights=avg_weights_np)
print("MEDIA PESATA:", media_pesata)
