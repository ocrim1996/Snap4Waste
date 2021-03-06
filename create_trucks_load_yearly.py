import os
import pandas as pd
import matplotlib.pyplot as plt
from settings import settings

trucks_load = pd.read_csv(os.path.join(settings.csv_folder, "ams_trucks_paths_yearly_14000_3000.csv"))

trucks_load['tot_weight'] = trucks_load.groupby(['date', 'truck_num'])['weight'].transform('sum')
trucks_load = trucks_load.drop_duplicates(subset=['date', 'truck_num'], keep='last')
trucks_load = trucks_load[['date', 'truck_num', 'tot_weight']]

trucks_load.to_csv(os.path.join(settings.csv_folder, "ams_trucks_load_yearly_14000_3000.csv"), encoding='utf-8', index=False)


step = [i for i in range(0, 14000, 100)]
col = trucks_load.tot_weight.to_list()
plt.hist(col, step, edgecolor='black', linewidth=1.2)

plt.title("Distribution trucks load")
plt.xlabel("Weight (kg)")
plt.ylabel("Frequency")
plt.savefig(os.path.join(settings.outputs_folder, "ams_distribution_trucks_load_14000_3000.jpeg"))
plt.show()

trucks_num = pd.read_csv(os.path.join(settings.csv_folder, "ams_trucks_load_yearly_14000_3000.csv"))
trucks_num = trucks_num.groupby(['date']).size().reset_index(name='tot_trucks')
trucks_num.to_csv(os.path.join(settings.csv_folder, "ams_trucks_num_14000_3000.csv"), encoding='utf-8', index=False)

step = [i for i in range(0, 75, 5)]
col2 = trucks_num.tot_trucks.to_list()
plt.hist(col2, step, edgecolor='black', linewidth=1.2)
plt.xticks(range(0, 75, 5))

plt.title("Distribution trucks num")
plt.xlabel("Number of trucks by day")
plt.ylabel("Frequency")
plt.savefig(os.path.join(settings.outputs_folder, "ams_distribution_trucks_num_14000_3000.jpeg"))
plt.show()


