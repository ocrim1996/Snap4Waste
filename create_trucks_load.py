import pandas as pd
import csv
from statistics import mean

trucks_load = pd.read_csv("trucks_paths.csv")
text = trucks_load['date'][0][:-14]

trucks_load['tot_weight'] = trucks_load.groupby(['truck_num'])['weight'].transform('sum')
trucks_load = trucks_load.drop_duplicates(subset=['truck_num'], keep='last')
trucks_load = trucks_load[['truck_num', 'tot_weight']]

trucks_load.to_csv("trucks_load.csv", encoding='utf-8', index=False)

with open("trucks_load.csv", 'r') as myfile:
    reader = csv.reader(myfile)
    skip = next(reader, None)
    trucks_path_weights = []
    for row in reader:
        trucks_path_weights.append(float(row[1]))

min_weights = min(trucks_path_weights)
max_weights = max(trucks_path_weights)
avg_weights = round(mean(trucks_path_weights), 2)
sum_daily_weights = sum(trucks_path_weights)

with open('trucks_stats.txt', 'w') as f:
    f.write("Raccolta giorno: " +str(text))
    f.write('\n')
    f.write("· Peso minimo camion a fine giro -> " + str(min_weights) + " Kg")
    f.write('\n')
    f.write("· Peso massimo camion a fine giro -> " + str(max_weights) + " Kg")
    f.write('\n')
    f.write("· Peso medio camion a fine giro -> " + str(avg_weights) + " Kg")
    f.write('\n')
    f.write("· Peso totale giornaliero -> " + str(sum_daily_weights) + " Kg")



