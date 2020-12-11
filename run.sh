#!/bin/bash

echo "running cron file"
if ! pgrep -f MQTT_logger.py
then
    echo "not running. firing up the logger"
    source /home/medadnew/virtualenv/HAB/3.6/bin/activate && cd /home/medadnew/HAB && nohup python MQTT_logger/MQTT_logger.py &
else
    echo "running"
fi

