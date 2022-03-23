import pandas as pd
import matplotlib.pyplot as plt

trucks_load = pd.read_csv("trucks_paths_yearly.csv")

trucks_load['tot_weight'] = trucks_load.groupby(['date', 'truck_num'])['weight'].transform('sum')
trucks_load = trucks_load.drop_duplicates(subset=['date', 'truck_num'], keep='last')
trucks_load = trucks_load[['date', 'truck_num', 'tot_weight']]

trucks_load.to_csv("trucks_load_yearly.csv", encoding='utf-8', index=False)

step = [i for i in range(0, 12000, 100)]
col = trucks_load.tot_weight.to_list()
plt.hist(col, step, edgecolor='black', linewidth=1.2)

plt.title("Distribution trucks load")
plt.xlabel("Weight (kg)")
plt.ylabel("Frequency")
plt.show()

trucks_num = pd.read_csv("trucks_load_yearly.csv")
trucks_num = trucks_num.groupby(['date']).size().reset_index(name='tot_trucks')
trucks_num.to_csv("trucks_num.csv", encoding='utf-8', index=False)

step = [i for i in range(0, 60, 5)]
col2 = trucks_num.tot_trucks.to_list()
plt.hist(col2, step, edgecolor='black', linewidth=1.2)
plt.xticks(range(0, 60, 5))

plt.title("Distribution trucks num")
plt.xlabel("Number of trucks by day")
plt.ylabel("Frequency")
plt.show()


