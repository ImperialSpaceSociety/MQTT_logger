from unittest import TestCase
from make_predictions_and_save import PredictionManager
from freezegun import freeze_time


class TestPredictionManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPredictionManager, self).__init__(*args, **kwargs)
        self.pm = PredictionManager()

    @freeze_time("2020-12-17 12:27:15")
    def test_gen_filename(self):
        res = self.pm.gen_filename("test")
        self.assertEqual(res,"test_2020-12-17_12-27-15.json")
