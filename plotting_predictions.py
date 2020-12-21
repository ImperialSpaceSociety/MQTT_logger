import json
from pathlib import Path

import pandas as pd
import plotly.express as px

fp = Path("datadump/forward_prediction_at_2020-12-21_00-00-02.json")


class PredictionPlotter:

    def plot(self, json_fp: Path):
        with open(str(json_fp)) as json_file:
            data = json.load(json_file)
            trajectory_dict = data["prediction"][1]["trajectory"]
            df = pd.DataFrame.from_dict(trajectory_dict)

            # Convert to datetime format. Have to remove last 3 decimal places for the parser to work
            df['datetime'] = df['datetime'].str.slice(0, -4)
            df['datetime_type'] = pd.to_datetime(df['datetime'])

            fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_data=["altitude", "datetime"], zoom=1)

            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            return fig

    def save_plot(self, fig):
        fig.write_html("plot.html")

    def show_plot(self, fig):
        fig.show()


if __name__ == "__main__":
    pp = PredictionPlotter()
    fig = pp.plot(json_fp=fp)
    pp.save_plot(fig)
    pp.show_plot(fig)

