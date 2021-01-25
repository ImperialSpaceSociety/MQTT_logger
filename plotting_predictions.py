import json
from pathlib import Path

import pandas as pd
import plotly.express as px
from pysolar.solar import get_altitude
from datetime import datetime, timedelta, timezone

from file_saver import data_dump_location, html_render_location


class PredictionPlotter:

    def plot(self, json_fp: Path):
        with open(str(json_fp)) as json_file:
            data = json.load(json_file)
            trajectory_dict = data["prediction"][1]["trajectory"]
            df = pd.DataFrame.from_dict(trajectory_dict)

            # Convert to datetime format. Have to remove last 3 decimal places for the parser to work
            df['datetime'] = df['datetime'].str.slice(0, -4)
            df['datetime_type'] = pd.to_datetime(df['datetime'])

            # Hacky section to calculate solar elevation for display.
            # TODO: convert this into more pandas/numpy form.
            ts_list = df["datetime_type"].dt.to_pydatetime().tolist()

            solar_elevation_list = []
            for i in range(len(ts_list)):
                elevation = get_altitude(longitude_deg=df["longitude"][i], latitude_deg=df["latitude"][i], when=ts_list[i].replace(tzinfo=timezone.utc))
                solar_elevation_list.append(elevation)

            df["solar_elevation"] = solar_elevation_list

            fig = px.line_geo(df, lat="latitude", lon="longitude", hover_data=["altitude", "datetime","solar_elevation"],
                              projection="orthographic",
                              )

            #fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_geos(
                resolution=110,
                showcountries=True
            )
            return fig

    def save_plot(self, fig):
        file_path = html_render_location / "plot.html"
        fig.write_html(str(file_path))

    def show_plot(self, fig):
        fig.show()

    def plot_and_save(self, json_fp: Path):
        p = self.plot(json_fp)
        self.save_plot(p)
