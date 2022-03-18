import pandas as pd

trucks_load = pd.read_csv("trucks_paths.csv")

trucks_load['tot_weight'] = trucks_load.groupby(['truck_num'])['weight'].transform('sum')
trucks_load = trucks_load.drop_duplicates(subset=['truck_num'], keep='last')
trucks_load = trucks_load[['truck_num', 'tot_weight']]

trucks_load.to_csv("trucks_load.csv", encoding='utf-8', index=False)