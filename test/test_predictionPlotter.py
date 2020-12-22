from pathlib import Path
from unittest import TestCase

from plotting_predictions import PredictionPlotter


class TestPredictionPlotter(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPredictionPlotter, self).__init__(*args, **kwargs)
        self.pp = PredictionPlotter()

    def test_plot_and_save(self):
        json_fp = Path("datadump/forward_prediction_at_2020-12-22_16-00-02.json")
        self.pp.plot_and_save(json_fp)
