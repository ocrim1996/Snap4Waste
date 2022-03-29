import os
import pandas as pd
from statistics import mean, median
from settings import settings

file1 = pd.read_csv(os.path.join(settings.csv_folder, "ams_trucks_num_12000.csv"))

trucks_num = file1.tot_trucks.to_list()

trucks_mean = mean(trucks_num)
trucks_median = median(trucks_num)

print("Numero medio di camion:", trucks_mean)
print("Numero mediano di camion:", trucks_median)
print("*"*50)

file2 = pd.read_csv(os.path.join(settings.csv_folder, "ams_trucks_load_yearly_12000.csv"))

load = file2.tot_weight.to_list()

load_mean = mean(load)
load_median = median(load)

print("Peso medio fine giro:", load_mean)
print("Peso mediano fine giro:", load_median)

