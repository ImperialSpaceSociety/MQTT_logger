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
from threading import Thread

import paho.mqtt.client as mqtt

from logger import init_logging
from packet_parser import PacketParser
from prediction_manager import PredictionManager
from plotting_predictions import PredictionPlotter
from file_saver import data_dump_location,html_render_location

init_logging()


class ThreadedMQTTLogger(Thread):
    def __init__(self, APPID, PSW):
        self.pm = PredictionManager()
        self.pp = PredictionPlotter()

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
            self.manage_incoming_packet(msg.payload)

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

    def manage_incoming_packet(self, incoming_pkt: str):
        """
        Save a flight prediction from the exact point the balloon was last seen
        :param incoming_pkt:
        :return: None
        """
        # parse packet
        parsed_pkt = PacketParser(incoming_pkt)  # TODO: figure out how to fake the parsed packet with current time.

        try:
            logging.debug("parsing incoming packet" + str(incoming_pkt))

            parsed_pkt.parse_packet()
        except ValueError:
            return

        filename = self.pm.gen_filename("prediction_at")
        self.pm.predict_and_save(parsed_pkt.current_time,
                                 parsed_pkt.current_alt,
                                 parsed_pkt.current_long,
                                 parsed_pkt.current_lat,
                                 filename)

        self.pp.plot_and_save(data_dump_location/filename)

if __name__ == "__main__":
    APPID = "icss_lora_tracker"
    PSW = 'ttn-account-v2.vlMjFic1AU9Dr-bAI18X6kzc5lSJGbFoeLbbASramBg'
    mqttlogger = ThreadedMQTTLogger(APPID, PSW)
    mqttlogger.start()
