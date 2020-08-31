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


import json
import logging
from threading import Thread

import paho.mqtt.client as  mqtt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("mqtt.log"),
        logging.StreamHandler()
    ]
)
# APPEUI = "70B3D57EF00069A3"
APPID = "icss_lora_tracker"
PSW = 'ttn-account-v2.vlMjFic1AU9Dr-bAI18X6kzc5lSJGbFoeLbbASramBg'


class ThreadedServer(Thread):
    def __init__(self):

        self.mqttc = mqtt.Client()
        # Assign event callbacks
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_log = self.on_log
        self.mqttc.on_publish = self.on_publish

        # mqttc.enable_logger(logger=None)
        self.mqttc.reconnect_delay_set(min_delay=1, max_delay=120)

        self.mqttc.username_pw_set(APPID, PSW)
        self.mqttc.connect("eu.thethings.network", 1883, 60)

        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        # and listen to server
        run = True
        while run:
            self.mqttc.loop()

    # gives connection message
    def on_connect(self, mqttc, mosq, obj, rc):
        print("Connected with result code:" + str(rc))
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
            x = json.loads(msg.payload.decode('utf-8'))

        except Exception as e:
            print(e)
            pass

    def on_publish(self, mosq, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, buf):
        print("message:" + str(buf))
        # print("userdata:" + str(obj))


def some_callback(client, address, data):
    print('data received', data.strip("\n"), flush=True)
    # send a response back to the client


if __name__ == "__main__":
    ThreadedServer().start()
