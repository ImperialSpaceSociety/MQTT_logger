from datetime import datetime, timedelta, timezone
from unittest import TestCase

from packet_parser import PacketParser


class Test_Scorer(TestCase):
    def setUp(self) -> None:
        self.raw_ttnv3_packet = '{"end_device_ids":{"device_id":"icspace26-ttnv3-abp-eu","application_ids":{"application_id":"icss-lora-tracker"},"dev_addr":"260B88E9"},"correlation_ids":["as:up:01F525MCNKSH62GJYG7NX6XTYB","ns:uplink:01F525MCF3RD7PTGA842BK4EV7","pba:conn:up:01F4S0EZVXS88GJ8THJ3HZ2ZE2","pba:uplink:01F525MCEP4MG9QSRRMF7NPPVB","rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01F525MCF3Y5HS4TF130Z9JMPZ","rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01F525MCNKFGAS2R6JJY239W8Q"],"received_at":"2021-05-07T01:03:52.500139766Z","uplink_message":{"f_port":99,"f_cnt":715,"frm_payload":"e8AAAxkAAAAAAAA=","rx_metadata":[{"gateway_ids":{"gateway_id":"packetbroker"},"packet_broker":{"message_id":"01F525MCEP4MG9QSRRMF7NPPVB","forwarder_net_id":"000013","forwarder_tenant_id":"ttn","forwarder_cluster_id":"ttn-v2-eu-1","home_network_net_id":"000013","home_network_tenant_id":"ttn","home_network_cluster_id":"ttn-eu1","hops":[{"received_at":"2021-05-07T01:03:52.278753207Z","sender_address":"52.169.73.251","receiver_name":"router-dataplane-57d9d9bddd-xjszp","receiver_agent":"pbdataplane/1.5.2 go/1.16.2 linux/amd64"},{"received_at":"2021-05-07T01:03:52.279636012Z","sender_name":"router-dataplane-57d9d9bddd-xjszp","sender_address":"forwarder_uplink","receiver_name":"router-5b5dc54cf7-mwf8m","receiver_agent":"pbrouter/1.5.2 go/1.16.2 linux/amd64"},{"received_at":"2021-05-07T01:03:52.281072832Z","sender_name":"router-5b5dc54cf7-mwf8m","sender_address":"deliver.000013_ttn_ttn-eu1.uplink","receiver_name":"router-dataplane-57d9d9bddd-f7h6k","receiver_agent":"pbdataplane/1.5.2 go/1.16.2 linux/amd64"}]},"time":"2021-05-07T01:03:52.253859996Z","rssi":-31,"channel_rssi":-31,"snr":8.75,"uplink_token":"eyJnIjoiWlhsS2FHSkhZMmxQYVVwQ1RWUkpORkl3VGs1VE1XTnBURU5LYkdKdFRXbFBhVXBDVFZSSk5GSXdUazVKYVhkcFlWaFphVTlwU1hoUldGcE9WV3N4YzAxc1FsbGxiRXBIWTFWS2JFbHBkMmxrUjBadVNXcHZhV1ZYY3pGT1Yxa3pWRlZLWm1WRmQzZFJhbGswVGxWc1NtSlhUbkZSVTBvNUxtOXNUM0ZJUjFOaU1tZG1UbFZEYlhCbGVYaExVbmN1TWs5ZlNVUk9PR3hyTkdOeVYyNDFPQzVoZVhwbllXVk9jelJxV0RoR2FGWjFiMXBwY1VVeGFrNWthemRYZEhOR1VURnJVRXN0ZFZSSGRXdFhVV0pWZGpkYVJGZG5ialZYVEVKc1Yyc3RMVU50TlUxcGFXOWZYekZhYWt4YVNWTXhVa2N6U3pGWVRIRldiV3d0ZVZodldFTjNjRlZGWkVkSGVrTkZUVVJ1UjJsSFpGSlVOVFZvVW1GdlJtVkZZMmxsTWxZMExXWmlXakpYVTI5TVRpMTFXR3N6ZUVRMGJHc3dOV2hzTkZSRVNYRm1WbVp2YjJReFNTNUthelIyU0Zsb04ybDRObWRFYkRRMFpIWmpVR1JSIiwiYSI6eyJmbmlkIjoiMDAwMDEzIiwiZnRpZCI6InR0biIsImZjaWQiOiJ0dG4tdjItZXUtMSJ9fQ=="}],"settings":{"data_rate":{"lora":{"bandwidth":125000,"spreading_factor":7}},"data_rate_index":5,"coding_rate":"4/5","frequency":"868300000"},"received_at":"2021-05-07T01:03:52.291333761Z","consumed_airtime":"0.061696s"}}'
        self.raw_mqtt_packet = '{"app_id":"icss_lora_tracker","dev_id":"icspace23","hardware_serial":"0093BECA9134091B","port":99,"counter":41,"payload_raw":"a03IKRX5Hs4ARgH6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgf6HtEA4wBCYQf6HtEACQFmYQf6HtEAhgIRfQf6HtEA6QAErgc=","metadata":{"time":"2020-12-15T13:32:30.644741305Z","frequency":868.1,"modulation":"LORA","data_rate":"SF8BW125","airtime":389632000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-0000024b0b03046b","timestamp":2834815476,"time":"2020-12-15T13:32:30.62244Z","channel":0,"rssi":-66,"snr":11.2,"rf_chain":0,"latitude":51.96731,"longitude":1.35357,"altitude":32}]}}'
        self.junk_mqtt_packet = '{"app_id":"icss_lora_tracker","dev_id":"icspace23","hardware_serial":"0093BECA9134091B","port":0,"counter":39,"payload_raw":null,"metadata":{"time":"2020-12-15T13:31:02.338677749Z","frequency":868.5,"modulation":"LORA","data_rate":"SF8BW125","airtime":82432000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-0000024b0b03046b","timestamp":2746508244,"time":"2020-12-15T13:31:02.315183Z","channel":2,"rssi":-67,"snr":9,"rf_chain":0,"latitude":51.96731,"longitude":1.35355,"altitude":32}]}}'
        self.test_raw_payload = "a0HKQBS3HuD/pP+3HuD/OQHkBbce4P8+Ae4Ftx7g/1QB6AW3HuD/SgHyBbce4P86AewFtx7g/zoB8AW3HuD/ZQHiBbce4P9NAeYFtx7g/yEBHgC3HuD/PgHqBbce4P85AeQFtx7g/z4B7gW3HuD/VAHoBQ=="

        self.current_time = datetime.strptime("2021-05-07T01:03:52.500139", '%Y-%m-%dT%H:%M:%S.%f')
        self.current_time = self.current_time.replace(tzinfo=timezone.utc)

    def test_parse_raw_packet(self):
        pac = PacketParser(raw_packet=self.raw_mqtt_packet)
        pac.parse_raw_payload(self.test_raw_payload, self.current_time)

        self.assertEqual(16688, pac.current_alt)
        self.assertEqual(8, pac.num_sats)
        self.assertAlmostEqual(-0.209712, pac.current_long, delta=0.00001)
        self.assertAlmostEqual(51.530170, pac.current_lat, delta=0.00001)


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

    def test_if_current_device_id_is_parsed_correctly(self):
        pac = PacketParser(raw_packet=self.raw_mqtt_packet)
        pac.parse_packet()

        self.assertEqual("icspace23", pac.device_id)

    def test_if_current_time_is_parsed_correctly(self):
        pac = PacketParser(raw_packet=self.raw_mqtt_packet)
        pac.parse_packet()
        target_time = datetime(2020, 12, 15, 13, 32, 30, tzinfo=timezone.utc)

        self.assertAlmostEqual(target_time, pac.current_time, delta=timedelta(seconds=1))

    def test_if_can_parse_junk_packet(self):
        pac = PacketParser(raw_packet=self.junk_mqtt_packet)

        self.assertRaises(ValueError, pac.parse_packet)

    def test_if_current_device_id_is_parsed_correctly_v3(self):
        pac = PacketParser(raw_packet=self.raw_ttnv3_packet)
        pac.parse_packet_v3()

        self.assertEqual("icspace26-ttnv3-abp-eu", pac.device_id)
