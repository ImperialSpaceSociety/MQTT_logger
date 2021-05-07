import base64
import json
from datetime import datetime
from datetime import timezone


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
        self.past_positions = []

    def parse_packet(self):
        payload_json = json.loads(self.raw_packet)

        date_time_str = payload_json["metadata"]["time"][:-4]
        self.current_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')
        self.current_time = self.current_time.replace(tzinfo=timezone.utc)

        self.device_id = payload_json["dev_id"]


        raw_payload = payload_json["payload_raw"]

        if raw_payload == None:
            raise ValueError("No payload found")

        self.parse_raw_payload(raw_payload, self.current_time)

    def parse_packet_v3(self):
        payload_json = json.loads(self.raw_packet)

        date_time_str = payload_json["received_at"][:-4]
        self.current_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')
        self.current_time = self.current_time.replace(tzinfo=timezone.utc)

        self.device_id = payload_json["end_device_ids"]["device_id"]


        raw_payload = payload_json["uplink_message"]["frm_payload"]

        if raw_payload == None:
            raise ValueError("No payload found")

        self.parse_raw_payload(raw_payload, self.current_time)


    def parse_raw_payload(self, raw_payload, current_time):

        hex_payload = base64.b64decode(raw_payload)

        self.pressure = ((hex_payload[2] >> 1) & 0b01111111) * 10
        self.reset_cnt = hex_payload[3] & 0b00000111
        self.boardTemp = int.from_bytes(hex_payload[4:5], byteorder="little", signed=True)
        self.noloadVoltage = ((hex_payload[0] >> 3) & 0b00011111) + 18
        self.loadVoltage = (((hex_payload[0] << 2) & 0b00011100) | ((hex_payload[1] >> 6) & 0b00000011)) + 18
        self.days_of_playback = hex_payload[1] & 0b00111111
        self.num_sats = hex_payload[3] >> 3 & 0b00011111
        self.current_long = int.from_bytes(hex_payload[7:9], byteorder="little", signed=True) * 0xffff / 1e7
        self.current_lat = int.from_bytes(hex_payload[5:7], byteorder="little", signed=True) * 0xffff / 1e7
        self.current_alt = int(int.from_bytes(hex_payload[9:11], byteorder="little", signed=False) * 0xff / 1000)

        past_data_size = 8  # Number of bytes to store one set of past long,lat,alt, timestamp

        self.past_positions = []
        for i in range(13):
            offset = (i + 1) * past_data_size
            current_long = int.from_bytes(hex_payload[13 + offset:15 + offset], byteorder="little",
                                          signed=True) * 0xffff / 1e7
            current_lat = int.from_bytes(hex_payload[11 + offset:13 + offset], byteorder="little",
                                         signed=True) * 0xffff / 1e7
            current_alt = int(
                int.from_bytes(hex_payload[15 + offset:17 + offset], byteorder="little", signed=False) * 0xff / 1000)
            time = datetime.fromtimestamp(
                datetime.timestamp(current_time) - int.from_bytes(hex_payload[17 + offset:19 + offset],
                                                                  byteorder="little", signed=False) * 60)

            past_pos = {
                "altitude": current_alt,
                "latitude": current_lat,
                "longitude": current_long,
                "time_stamp": time
            }

            self.past_positions.append(past_pos)
