from pathlib import Path
from unittest import TestCase

from plotting_predictions import PredictionPlotter


class TestPredictionPlotter(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPredictionPlotter, self).__init__(*args, **kwargs)
        self.pp = PredictionPlotter()

    def test_plot_and_save(self):
        json_fp = Path("datadump/forward_prediction_at_2020-12-23_16-00-01.json")
        self.pp.plot_and_save(json_fp)

    def test_plot_and_show(self):
        json_fp = Path("datadump/forward_prediction_at_2020-12-23_16-00-01.json")
        p = self.pp.plot(json_fp)
        self.pp.show_plot(p)
