import time
from datetime import datetime

import re
import time
from datetime import datetime
from pathlib import Path
import json
import pandas as pd
import schedule
from bisect import bisect_left, bisect_right
from logger import init_logging
from make_predictions_and_save import PredictionManager
init_logging()



from file_saver import FileSaver
from prediction_api_client import PredictApiClient
regex_time_str = re.compile(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})")

class PredictionSaver:
    def __init__(self):
        self.predictapiclient = PredictApiClient()
        self.filesaver = FileSaver()
        self.pm = PredictionManager()

    @staticmethod
    def extract_datetimes(string):
        year, month, day, hour, minute, sec = re.search(regex_time_str,string).groups()
        target_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec))

        return target_time

    def get_latest_prediction_json_file(self):
        p = Path(r'datadump/')
        onlyfiles = p.rglob('*')

        sortedFiles = sorted(onlyfiles, key=lambda x: self.extract_datetimes(str(x)))
        return sortedFiles[-1]

    def get_predicted_position_from_prediction_file_at_specified_timestamp(self, prediction_file: Path, timestamp):

        df = pd.DataFrame()
        with open(str(prediction_file)) as json_file:
            data = json.load(json_file)
            trajectory_dict = data["prediction"][1]["trajectory"]
            df = pd.DataFrame.from_dict(trajectory_dict)

            # Convert to datetime format. Have to remove last 3 decimal places for the parser to work
            df['datetime'] = df['datetime'].str.slice(0, -4)
            df['datetime_type'] = pd.to_datetime(df['datetime'])

        # times stamps are sorted list so we can use bisect function to get the exact row
        idx = bisect_left(df['datetime_type'].values, timestamp)


        return df.at[idx,'longitude'], df.at[idx,'latitude'],df.at[idx,'altitude']

    def save_prediction_on_past_prediction(self):
        """
        Run a prediction from the position the last prediction expected the balloon to be at.
        This will update the prediction as time goes by
        :return:
        """

        current_time = pd.Timestamp.now()
        latest_prediction_file = self.get_latest_prediction_json_file()
        long,lat,alt = self.get_predicted_position_from_prediction_file_at_specified_timestamp(latest_prediction_file,current_time)

        self.pm.predict_and_save(datetime.now(),alt,long,lat,"forward_prediction_at")


if __name__ == "__main__":

    ps = PredictionSaver()
    ps.save_prediction_on_past_prediction()


    schedule.every().hour.at("00:00").do(ps.save_prediction_on_past_prediction)

    while True:
        schedule.run_pending()
        time.sleep(1)
