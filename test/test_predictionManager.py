from unittest import TestCase
from prediction_manager import PredictionManager
from freezegun import freeze_time
from datetime import datetime

target_url = "http://predict.cusf.co.uk/api/v1/?launch_latitude=52&launch_longitude=0&launch_altitude=11999&launch_datetime=2020-12-17T11%3A30%3A00%2B00%3A00&ascent_rate=0.8&float_altitude=12000&stop_datetime=2020-12-20T11%3A30%3A00%2B00%3A00&profile=float_profile"

class TestPredictionManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPredictionManager, self).__init__(*args, **kwargs)
        self.pm = PredictionManager()

    @freeze_time("2020-12-17 12:27:15")
    def test_gen_filename(self):
        res = self.pm.gen_filename("test")
        self.assertEqual(res,"test_2020-12-17_12-27-15.json")

    def test_if_prediction_request_url_is_correct(self):
        res = self.pm.make_request(start_time=datetime(2020, 12, 17, 11, 30, 00), hours_ahead=72, current_alt=12000,
                               current_long=0, current_lat=52)
        self.assertEqual(target_url, res.url)

    def test_if_prediction_api_is_working(self):
        res = self.pm.make_request(start_time=datetime.now(), hours_ahead=72, current_alt=12000,
                               current_long=0, current_lat=52)
        keys = res.json().keys()
        self.assertNotIn('error',keys)

    def test_if_prediction_api_is_not_working(self):
        res = self.pm.make_request(start_time=datetime(2020, 12, 15, 11, 30, 00), hours_ahead=72, current_alt=12000,
                               current_long=0, current_lat=52)
        keys = res.json().keys()
        self.assertIn('error',keys)