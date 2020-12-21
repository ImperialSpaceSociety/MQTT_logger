from datetime import datetime
from pathlib import Path
from unittest import TestCase

import pandas as pd

from make_periodic_prediction import PredictionSaver


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
    def test_2_extract_datetimes_with_different_prefix(self):
        filename_str = "datadump/prediction_at_2020-12-18_11-55-08.json"
        dt = self.ps.extract_datetimes(filename_str)

        expected_datetime = datetime(2020, 12, 18, 11, 55, 8)

        self.assertEqual(expected_datetime, dt)

    def test_get_latest_prediction_json_file(self):
        p = Path(r'../datadump/')

        latest_file = self.ps.get_latest_prediction_json_file(p)
        self.assertEqual(Path("../datadump/prediction_at_2020-12-18_12-54-25.json"), latest_file)

    def test_get_predicted_position_from_prediction_file_at_specified_timestamp(self):
        fp = Path("../datadump/prediction_at_2020-12-18_12-54-25.json")

        expected_time = pd.Timestamp(year=2020,month=12,day=19,hour=1,minute=46,second=7)

        lat, long, alt = self.ps.get_predicted_position_from_prediction_file_at_specified_timestamp(fp, expected_time)
        self.assertAlmostEqual(41.549955394115386, lat,delta=0.1)
        self.assertAlmostEqual(56.15682667133098, long,delta=0.1)
        self.assertAlmostEqual(10602, alt,delta=1)

    def test_save_prediction_on_past_prediction(self):
        self.ps.save_prediction_on_past_prediction()
