########################################################################################################################
#
# Created: 31/08/2020
# Author: Medad Newman
#
# Get data from MQTT server
# Run this with python 3, install paho.mqtt prior to use
# https://www.thethingsnetwork.org/forum/t/a-python-program-to-listen-to-your-devices-with-mqtt/9036/6
#
# threaded example credit; https://forum.derivative.ca/t/python-threaded-tcp-socket-server-example/12002/5
########################################################################################################################


import logging
import sys
from datetime import datetime
from threading import Thread

import paho.mqtt.client as mqtt

from file_saver import FileSaver
from packet_parser import PacketParser
from prediction_api_client import PredictApiClient

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('mqtt.txt')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)


class ThreadedMQTTLogger(Thread):
    def __init__(self, APPID, PSW):
        self.predictapiclient = PredictApiClient()
        self.filesaver = FileSaver()

        self.mqttc = mqtt.Client()
        # Assign event callbacks
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_log = self.on_log
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_disconnect = self.on_disconnect

        self.__reconnect = True

        # mqttc.enable_logger(logger=None)
        self.mqttc.reconnect_delay_set(min_delay=1, max_delay=120)

        self.mqttc.username_pw_set(APPID, PSW)
        self.mqttc.connect("eu.thethings.network", 1883, 60)

        Thread.__init__(self)
        logging.info("Running MQTT Logger")

    # run by the Thread object
    def run(self):
        logging.info("Starting MQTT logger thread")

        # and listen to server
        run = True
        while run:
            self.mqttc.loop()

    # gives connection message
    def on_connect(self, mqttc, mosq, obj, rc):
        logging.debug("Connected with result code:" + str(rc))

        if rc == 0:
            # subscribe for all devices of user
            res_1 = mqttc.subscribe('+/devices/+/up')
            res = mqttc.subscribe('+/devices/+/events/#')

            if res[0] != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError("the client is not connected")

    # gives message from device
    def on_message(self, mqttc, obj, msg):
        try:
            logging.info(msg.payload)
            self.save_prediction(msg.payload)

        except Exception as e:
            logging.critical(e, exc_info=True)  # log exception info at CRITICAL log level

    def on_publish(self, mosq, obj, mid):
        logging.debug("mid: " + str(mid))

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        logging.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, buf):
        logging.debug("message:" + str(buf))

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            if self.__reconnect:
                self.mqttc.reconnect()
            else:
                logging.error("unexpected disconnection")

    def save_prediction(self, incoming_pkt: str):
        """
        Save a flight prediction from the exact point the balloon was last seen
        :param incoming_pkt:
        :return: None
        """
        # parse packet
        parsed_pkt = PacketParser(incoming_pkt) # TODO: figure out how to fake the parsed packet with current time.

        try:
            logging.debug("parsing incoming packet" + str(incoming_pkt))

            parsed_pkt.parse_packet()
        except ValueError:
            return

        # request prediction of flight
        prediction = self.predictapiclient.make_request(parsed_pkt.current_time,
                                                        180,
                                                        parsed_pkt.current_alt,
                                                        parsed_pkt.current_long,
                                                        parsed_pkt.current_lat)
        # save prediction to file.
        file_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = 'prediction_at_{0}.json'.format(file_time)
        self.filesaver.save_file(file_name, prediction.content)


if __name__ == "__main__":
    APPID = "icss_lora_tracker"
    PSW = 'ttn-account-v2.vlMjFic1AU9Dr-bAI18X6kzc5lSJGbFoeLbbASramBg'
    mqttlogger = ThreadedMQTTLogger(APPID, PSW)
    mqttlogger.start()
