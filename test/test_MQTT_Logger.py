import unittest
from unittest import TestCase

from MQTT_logger import ThreadedMQTTLogger


class Testing_MQTT_Logger(TestCase):
    def setUp(self) -> None:

        APPID = "icss_lora_tracker"
        PSW = 'ttn-account-v2.vlMjFic1AU9Dr-bAI18X6kzc5lSJGbFoeLbbASramBg'
        self.TML = ThreadedMQTTLogger(APPID, PSW)
        self.raw_mqtt_packet = '{"app_id":"icss_lora_tracker","dev_id":"icspace23","hardware_serial":"0093BECA9134091B","port":99,"counter":41,"payload_raw":"a03IKRX5Hs4ARgH6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgc=","metadata":{"time":"2020-12-15T13:32:30.644741305Z","frequency":868.1,"modulation":"LORA","data_rate":"SF8BW125","airtime":389632000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-0000024b0b03046b","timestamp":2834815476,"time":"2020-12-15T13:32:30.62244Z","channel":0,"rssi":-66,"snr":11.2,"rf_chain":0,"latitude":51.96731,"longitude":1.35357,"altitude":32}]}}'
        self.mqtt_packet_with_none_payload = '{"app_id":"icss_lora_tracker","dev_id":"icspace23","hardware_serial":"0093BECA9134091B","port":0,"counter":39,"payload_raw":null,"metadata":{"time":"2020-12-15T13:31:02.338677749Z","frequency":868.5,"modulation":"LORA","data_rate":"SF8BW125","airtime":82432000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-0000024b0b03046b","timestamp":2746508244,"time":"2020-12-15T13:31:02.315183Z","channel":2,"rssi":-67,"snr":9,"rf_chain":0,"latitude":51.96731,"longitude":1.35355,"altitude":32}]}}'
        self.current_mqtt_packet = '{"app_id":"icss_lora_tracker","dev_id":"icspace23","hardware_serial":"0093BECA9134091B","port":99,"counter":41,"payload_raw":"a03IKRX5Hs4ARgH6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgc=","metadata":{"time":"2020-12-17T13:32:30.644741305Z","frequency":868.1,"modulation":"LORA","data_rate":"SF8BW125","airtime":389632000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-0000024b0b03046b","timestamp":2834815476,"time":"2020-12-15T13:32:30.62244Z","channel":0,"rssi":-66,"snr":11.2,"rf_chain":0,"latitude":51.96731,"longitude":1.35357,"altitude":32}]}}'

    def test_parsing_valid_packet(self):
        self.TML.manage_incoming_packet(self.raw_mqtt_packet)

    def test_parsing_future_valid_packet(self):
        self.TML.manage_incoming_packet(self.current_mqtt_packet)

    def test_parsing_invalid_packet(self):
        self.TML.manage_incoming_packet(self.mqtt_packet_with_none_payload)


if __name__ == '__main__':
    unittest.main()
