from datetime import datetime
from unittest import TestCase

from make_periodic_prediction import PredictionSaver
from pathlib import Path

class TestPredictionSaver(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPredictionSaver, self).__init__(*args, **kwargs)

        self.ps = PredictionSaver()

    def test_extract_datetimes(self):
        filename_str = "prediction_at_2020-12-17_14-52-19.json"
        dt = self.ps.extract_datetimes(filename_str)

        expected_datetime = datetime(2020, 12, 17, 14, 52, 19)

        self.assertEqual(expected_datetime, dt)

    def test_extract_datetimes_with_different_prefix(self):
        filename_str = "test_prediction_at_2020-12-17_14-52-19.json"
        dt = self.ps.extract_datetimes(filename_str)

        expected_datetime = datetime(2020, 12, 17, 14, 52, 19)

        self.assertEqual(expected_datetime, dt)

    def test_get_latest_prediction_json_file(self):
        latest_file = self.ps.get_latest_prediction_json_file()
        self.assertEqual(Path("../datadump/prediction_at_2020-12-18_12-54-25.json"),latest_file)


    # def test_get_latest_prediction(self):
    #     self.fail()

    # def test_save_prediction(self):
    #     self.fail()
