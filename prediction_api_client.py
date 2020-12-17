from datetime import datetime, timedelta

import requests

BASE_URL = "http://predict.cusf.co.uk/api/v1/"




class PredictApiClient:
    def __init__(self):
        pass

    def make_request(self, start_time: datetime, hours_ahead: int, current_alt, current_long, current_lat):
        params = {
            "launch_latitude": current_lat,
            "launch_longitude": current_long,
            "launch_altitude": current_alt-1,
            "launch_datetime": start_time.astimezone().isoformat(),
            "ascent_rate": 0.8,
            "float_altitude": current_alt,
            "stop_datetime": (start_time + timedelta(hours=hours_ahead)).astimezone().isoformat(),
            "profile": "float_profile"

        }
        return requests.get(BASE_URL, params=params)
