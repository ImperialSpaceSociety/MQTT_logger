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


    def parse_packet(self):
        payload_json = json.loads(self.raw_packet)

        date_time_str = payload_json["metadata"]["time"][:-4]
        self.current_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')


        raw_payload = payload_json["payload_raw"]

        if raw_payload == None:
            raise ValueError("No payload found")


        hex_payload = base64.b64decode(raw_payload)

        self.current_long = int.from_bytes(hex_payload[7:9], byteorder="little", signed=True) * 0xffff / 1e7
        self.current_lat = int.from_bytes(hex_payload[5:7], byteorder="little", signed=True) * 0xffff / 1e7
        self.current_alt = int(int.from_bytes(hex_payload[9:11], byteorder="little", signed=False) * 0xff / 1000)