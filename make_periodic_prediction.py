import time
from datetime import datetime

import re
import time
from datetime import datetime
from pathlib import Path


import schedule

from file_saver import FileSaver
from prediction_api_client import PredictApiClient
regex_time_str = re.compile(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})")

class PredictionSaver:
    def __init__(self):
        schedule.every().hour.at("00:00").do(self.save_prediction)
        self.predictapiclient = PredictApiClient()
        self.filesaver = FileSaver()

    @staticmethod
    def extract_datetimes(string):
        year, month, day, hour, minute, sec = re.search(regex_time_str,string).groups()
        target_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec))

        return target_time

    def get_latest_prediction_json_file(self):
        p = Path(r'../datadump/')
        onlyfiles = p.rglob('*')

        sortedFiles = sorted(onlyfiles, key=lambda x: self.extract_datetimes(str(x)))
        return sortedFiles[-1]

    def save_prediction(self):
        """
        :param incoming_pkt:
        :return: None
        """

        # request prediction of flight
        prediction = self.predictapiclient.make_request(datetime.now(),
                                                        180,
                                                        parsed_pkt.current_alt,
                                                        parsed_pkt.current_long,
                                                        parsed_pkt.current_lat)
        # save prediction to file.
        file_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = 'prediction_at_{0}.json'.format(file_time)
        self.filesaver.save_file(file_name, prediction.content)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
