import pandas as pd
import plotly.express as px

legend_dict = dict(
        x=0,
        y=1,
        title_font_family="Times New Roman",
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),
        bgcolor="#f0f3ef",
        bordercolor="Black",
        borderwidth=2
    )


def build_map(csv_file, text):
    container_pos = pd.read_csv(csv_file)

    fig = px.line_mapbox(container_pos, lat="lat", lon="long", hover_name="sum_weight", text="date", color="truck_num", zoom=3)

    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=11, mapbox_center_lat=52.370579,
                      mapbox_center_lon=4.902242, legend=legend_dict, margin={"r":0,"t":0,"l":0,"b":0})

    fig.add_annotation(
        text=text,
        xref="paper",
        yref="paper",
        align="left",
        x=0.99,
        y=0.98,
        showarrow=False,
        font=dict(
            family="Courier",
            size=10,
            color="black"
        ),
        bgcolor="#f0f3ef",
        bordercolor="Black",
        borderwidth=2
    )

    fig.show()

