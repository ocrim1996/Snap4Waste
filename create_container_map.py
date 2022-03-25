import os
import pandas as pd
import plotly.express as px
from settings import settings

csv_file = os.path.join(settings.csv_folder, "ams_id_list_rest_stats.csv")

container_pos = pd.read_csv(csv_file)

fig = px.scatter_mapbox(container_pos, lat="lat", lon="long", color="container_type", hover_name="id")

fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=11, mapbox_center_lat=52.370579,
                  mapbox_center_lon=4.902242, margin={"r":0,"t":0,"l":0,"b":0})

fig.show()