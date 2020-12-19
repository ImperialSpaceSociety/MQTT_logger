from file_saver import FileSaver
from prediction_api_client import PredictApiClient
from datetime import datetime

class PredictionManager:
    def __init__(self):
        self.predictapiclient = PredictApiClient()
        self.filesaver = FileSaver()

    def predict_and_save(self, ts, alt, long, lat, file_str_format):
        # request prediction of flight
        prediction = self.predictapiclient.make_request(ts, 180, alt, long, lat)
        # save prediction to file.
        file_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = file_str_format + '_{0}.json'.format(file_time)
        self.filesaver.save_file(file_name, prediction.content)