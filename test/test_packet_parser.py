from datetime import datetime, timedelta
from unittest import TestCase

from packet_parser import PacketParser


class Test_Scorer(TestCase):
    def setUp(self) -> None:
        self.raw_mqtt_packet = '{"app_id":"icss_lora_tracker","dev_id":"icspace23","hardware_serial":"0093BECA9134091B","port":99,"counter":41,"payload_raw":"a03IKRX5Hs4ARgH6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgc=","metadata":{"time":"2020-12-15T13:32:30.644741305Z","frequency":868.1,"modulation":"LORA","data_rate":"SF8BW125","airtime":389632000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-0000024b0b03046b","timestamp":2834815476,"time":"2020-12-15T13:32:30.62244Z","channel":0,"rssi":-66,"snr":11.2,"rf_chain":0,"latitude":51.96731,"longitude":1.35357,"altitude":32}]}}'
        self.junk_mqtt_packet = '{"app_id":"icss_lora_tracker","dev_id":"icspace23","hardware_serial":"0093BECA9134091B","port":0,"counter":39,"payload_raw":null,"metadata":{"time":"2020-12-15T13:31:02.338677749Z","frequency":868.5,"modulation":"LORA","data_rate":"SF8BW125","airtime":82432000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-0000024b0b03046b","timestamp":2746508244,"time":"2020-12-15T13:31:02.315183Z","channel":2,"rssi":-67,"snr":9,"rf_chain":0,"latitude":51.96731,"longitude":1.35355,"altitude":32}]}}'

    def test_if_current_long_is_parsed_correctly(self):
        pac = PacketParser(raw_packet=self.raw_mqtt_packet)
        pac.parse_packet()

        self.assertAlmostEqual(1.350021004, pac.current_long, delta=0.00001)

    def test_if_current_lat_is_parsed_correctly(self):
        pac = PacketParser(raw_packet=self.raw_mqtt_packet)
        pac.parse_packet()

        self.assertAlmostEqual(51.96269989, pac.current_lat, delta=0.00001)

    def test_if_current_alt_is_parsed_correctly(self):
        pac = PacketParser(raw_packet=self.raw_mqtt_packet)
        pac.parse_packet()

        self.assertAlmostEqual(83, pac.current_alt, delta=0.00001)

    def test_if_current_time_is_parsed_correctly(self):
        pac = PacketParser(raw_packet=self.raw_mqtt_packet)
        pac.parse_packet()
        target_time = datetime(2020, 12, 15, 13, 32, 30)

        self.assertAlmostEqual(target_time, pac.current_time, delta=timedelta(seconds=1))

    def test_if_can_parse_junk_packet(self):
        pac = PacketParser(raw_packet=self.junk_mqtt_packet)

        self.assertRaises(ValueError,pac.parse_packet)
