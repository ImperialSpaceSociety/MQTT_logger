# https://www.thethingsnetwork.org/forum/t/a-python-program-to-listen-to-your-devices-with-mqtt/9036/6
# Get data from MQTT server
# Run this with python 3, install paho.mqtt prior to use

import json
import logging

import paho.mqtt.client as mqtt

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


# Call back functions

# gives connection message
def on_connect(mqttc, mosq, obj, rc):
    print("Connected with result code:" + str(rc))
    if rc == 0:
        # subscribe for all devices of user
        res_1 = mqttc.subscribe('+/devices/+/up')
        res = mqttc.subscribe('+/devices/+/events/#')

        if res[0] != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError("the client is not connected")


# gives message from device
def on_message(mqttc, obj, msg):
    try:
        logging.info(msg.payload)
        x = json.loads(msg.payload.decode('utf-8'))

    except Exception as e:
        print(e)
        pass


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, buf):
    print("message:" + str(buf))
    # print("userdata:" + str(obj))


mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
# mqttc.on_log = on_log
mqttc.on_publish = on_publish

# mqttc.enable_logger(logger=None)
mqttc.reconnect_delay_set(min_delay=1, max_delay=120)

mqttc.username_pw_set(APPID, PSW)
mqttc.connect("eu.thethings.network", 1883, 60)

# and listen to server
run = True
while run:
    mqttc.loop()
