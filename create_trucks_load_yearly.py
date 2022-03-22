import pandas as pd
import csv
from statistics import mean

trucks_load = pd.read_csv("trucks_paths_yearly.csv")

trucks_load['tot_weight'] = trucks_load.groupby(['date', 'truck_num'])['weight'].transform('sum')
trucks_load = trucks_load.drop_duplicates(subset=['date', 'truck_num'], keep='last')
trucks_load = trucks_load[['date', 'truck_num', 'tot_weight']]

trucks_load.to_csv("trucks_load_yearly.csv", encoding='utf-8', index=False)