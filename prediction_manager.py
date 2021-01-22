from datetime import datetime, timedelta

import requests

from file_saver import FileSaver

BASE_URL = "http://predict.cusf.co.uk/api/v1/"


class PredictionManager:
    def __init__(self):
        self.filesaver = FileSaver()

    def predict_and_save(self, ts, alt, long, lat, file_name):
        # request prediction of flight
        prediction = self.make_request(ts, 120, alt, long, lat)
        # save prediction to file.
        self.filesaver.save_file(file_name, prediction.content)

    @staticmethod
    def gen_filename(file_str_prefix):
        file_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = '{0}_{1}.json'.format(file_str_prefix, file_time)
        return file_name

    def make_request(self, start_time: datetime, hours_ahead: int, current_alt, current_long, current_lat):
        params = {
            "launch_latitude": current_lat,
            "launch_longitude": current_long,
            "launch_altitude": current_alt - 1,
            "launch_datetime": start_time.astimezone().isoformat(),
            "ascent_rate": 0.8,
            "float_altitude": current_alt,
            "stop_datetime": (start_time + timedelta(hours=hours_ahead)).astimezone().isoformat(),
            "profile": "float_profile"

        }
        return requests.get(BASE_URL, params=params)
