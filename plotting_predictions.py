import json
from pathlib import Path

import pandas as pd
import plotly.express as px

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

            fig = px.line_geo(df, lat="latitude", lon="longitude", hover_data=["altitude", "datetime"],
                              projection="orthographic",
                              )

            #fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            return fig

    def save_plot(self, fig):
        file_path = html_render_location / "plot.html"
        fig.write_html(str(file_path))

    def show_plot(self, fig):
        fig.show()

    def plot_and_save(self, json_fp: Path):
        p = self.plot(json_fp)
        self.save_plot(p)
