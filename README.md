# MQTT_logger
A small repo that contains the logger for our pico balloon data, taking the data from the Things Network broker

Install the required packages with `pip3 install -r requirements.txt`.

The APPID and PSW are hardcoded into the program. Change them in `MQTT_logger.py` before using. Run `python3 MQTT_logger.py` to start the logger. The logs will be appended to mqtt.txt
The program has been only tested on Python 3.7
