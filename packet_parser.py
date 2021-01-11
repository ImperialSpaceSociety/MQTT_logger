import base64
import json
from datetime import datetime

class PacketParser:
    def __init__(self, raw_packet):
        self.raw_packet = raw_packet
        self.current_long = 0
        self.current_lat = 0
        self.current_alt = 0
        self.current_time = 0
        self.num_sats = 0
        self.days_of_playback = 0
        self.noloadVoltage = 0
        self.loadVoltage = 0
        self.pressure = 0
        self.reset_cnt = 0
        self.boardTemp = 0
        self.device_id = ""


    def parse_packet(self):
        payload_json = json.loads(self.raw_packet)

        date_time_str = payload_json["metadata"]["time"][:-4]
        self.current_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')
        self.device_id = payload_json["dev_id"]


        raw_payload = payload_json["payload_raw"]

        if raw_payload == None:
            raise ValueError("No payload found")


        self.parse_raw_payload(raw_payload)

    def parse_raw_payload(self,raw_payload):

        hex_payload = base64.b64decode(raw_payload)

        self.pressure = ((hex_payload[2] >> 1) & 0b01111111) * 10
        self.reset_cnt = hex_payload[3] & 0b00000111
        self.boardTemp = hex_payload[4]
        self.noloadVoltage = ((hex_payload[0] >> 3) & 0b00011111) + 18
        self.loadVoltage = (((hex_payload[0] << 2) & 0b00011100) | ((hex_payload[1] >> 6) & 0b00000011)) + 18
        self.days_of_playback = hex_payload[1] & 0b00111111
        self.num_sats = hex_payload[3] >> 3 & 0b00011111
        self.current_long = int.from_bytes(hex_payload[7:9], byteorder="little", signed=True) * 0xffff / 1e7
        self.current_lat = int.from_bytes(hex_payload[5:7], byteorder="little", signed=True) * 0xffff / 1e7
        self.current_alt = int(int.from_bytes(hex_payload[9:11], byteorder="little", signed=False) * 0xff / 1000)