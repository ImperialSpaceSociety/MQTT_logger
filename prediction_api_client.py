from requests import Session, Request
from datetime import datetime, timezone, timedelta

BASE_URL = "http://predict.cusf.co.uk/api/v1/"


# http://predict.cusf.co.uk/api/v1/?launch_latitude=52&launch_longitude=0&launch_altitude=0&launch_datetime=2020-12-09T11%3A30%3A00%2B00:00&ascent_rate=0.8&float_altitude=12000&stop_datetime=2020-12-15T11%3A30%3A00%2B00:00&profile=float_profile


class PredictApiClient:
    def __init__(self):
        pass

    def make_request(self,start_time,end_time):


        params = {
            "launch_latitude": 52,
            "launch_longitude": 0,
            "launch_altitude": 0,
            "launch_datetime": start_time,
            "ascent_rate": 0.8,
            "float_altitude": 12000,
            "stop_datetime": end_time,
            "profile": "float_profile"

        }

        s = Session()
        p = Request('GET', BASE_URL, params=params).prepare()
        r = s.send(p)

        #print(r.content)

        return p.url
