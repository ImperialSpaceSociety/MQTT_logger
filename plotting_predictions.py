import json
from pathlib import Path
import plotly.express as px

import pandas as pd
from matplotlib import pyplot as plt

fp = Path("datadump/prediction_at_2020-12-18_12-54-25.json")

with open(str(fp)) as json_file:
    data = json.load(json_file)
    trajectory_dict = data["prediction"][1]["trajectory"]
    df = pd.DataFrame.from_dict(trajectory_dict)

    # Convert to datetime format. Have to remove last 3 decimal places for the parser to work
    df['datetime'] = df['datetime'].str.slice(0, -4)
    df['datetime_type'] = pd.to_datetime(df['datetime'])

    plt.plot(df["longitude"], df["latitude"])
    #plt.show()


    #fig = px.scatter_mapbox(concatenated_df, lat="LOCATION Latitude : ", lon="LOCATION Longitude : ",color="LOCATION Speed ( Kmh)")
    #fig = px.scatter_mapbox(concatenated_df, lat="LOCATION Latitude : ", lon="LOCATION Longitude : ",color="abs_acceleration")
    #fig = px.scatter_mapbox(concatenated_df, lat="LOCATION Latitude : ", lon="LOCATION Longitude : ",color="gps_acceleration")
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_data=["datetime"])

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
