import json
import logging
import re
import time
from bisect import bisect_left
from datetime import datetime
from pathlib import Path
from plotting_predictions import PredictionPlotter
import pandas as pd
import schedule

from logger import init_logging
from prediction_manager import PredictionManager

init_logging()

from file_saver import FileSaver, data_dump_location

regex_time_str = re.compile(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})")


class PredictionSaver:
    def __init__(self):
        self.filesaver = FileSaver()
        self.pm = PredictionManager()
        logging.debug("Initialised periodic prediction saver")
        self.pp = PredictionPlotter()


    @staticmethod
    def extract_datetimes(string):
        year, month, day, hour, minute, sec = re.search(regex_time_str, string).groups()
        target_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec))

        return target_time

    def get_latest_prediction_json_file(self, p):
        """
        Search the supplied directory p for the most recent prediction json
        :param p: Pathlib object of directory to search
        :return: Pathlib object of more recent prediction json file.
        """
        onlyfiles = p.rglob('*')
        latest = self.get_latest_file_from_file_list(onlyfiles)
        return latest

    def get_latest_file_from_file_list(self, file_list: list):
        sortedFiles = sorted(file_list, key=lambda x: self.extract_datetimes(str(x)))
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

        return df.at[idx, 'longitude'], df.at[idx, 'latitude'], df.at[idx, 'altitude']

    def save_prediction_on_past_prediction(self):
        """
        Run a prediction from the position the last prediction expected the balloon to be at.
        This will update the prediction as time goes by
        :return:
        """
        logging.debug("Saving prediction on past prediction")
        current_time = pd.Timestamp.now()

        latest_prediction_file = self.get_latest_prediction_json_file(data_dump_location)
        long, lat, alt = self.get_predicted_position_from_prediction_file_at_specified_timestamp(latest_prediction_file,
                                                                                                 current_time)
        logging.debug("Balloon expected to be long={0} lat={1} alt={2} now".format(long, lat, alt))

        filename = self.pm.gen_filename("forward_prediction_at")
        self.pm.predict_and_save(datetime.now(), alt, long, lat, filename)
        self.pp.plot_and_save(data_dump_location/filename)


if __name__ == "__main__":

    ps = PredictionSaver()
    logging.info("scheduling jobs for periodic running of predictions")
    ps.save_prediction_on_past_prediction()

    job = ps.save_prediction_on_past_prediction
    schedule.every().day.at("00:00").do(job)
    schedule.every().day.at("04:00").do(job)
    schedule.every().day.at("08:00").do(job)
    schedule.every().day.at("12:00").do(job)
    schedule.every().day.at("16:00").do(job)
    schedule.every().day.at("20:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
