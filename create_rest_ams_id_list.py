import os
import glob
import pandas as pd
from settings import settings


interesting_files = glob.glob("rest_mes_amsterdam_api/*.csv")
df = pd.concat((pd.read_csv(f, header = 0) for f in interesting_files))

df.to_csv(os.path.join(settings.csv_folder, "ams_id_list_rest.csv"), index=False)


# assign dataset
data = pd.read_csv(os.path.join(settings.csv_folder, "ams_id_list_rest.csv"))

# sort data frame
data.sort_values(["id", "dateObserved"], axis=0, ascending=[True, True], inplace=True)

data.to_csv(os.path.join(settings.csv_folder, "ams_id_list_rest_sorted.csv"), index=False)
