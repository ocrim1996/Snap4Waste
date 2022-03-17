import pandas as pd
import plotly.express as px


def build_map(csv_file):
    container_pos = pd.read_csv(csv_file)

    fig = px.line_mapbox(container_pos, lat="lat", lon="long", text="date", color="truck_num", zoom=3)

    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=11, mapbox_center_lat=52.370579,
                      mapbox_center_lon=4.902242, margin={"r":0,"t":0,"l":0,"b":0})

    fig.show()

