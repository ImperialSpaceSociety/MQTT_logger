#!/bin/bash
# TO be placed in `export VISUAL=nano; crontab -e` with the following entry
#
#MAILTO="mailto@medadnewman.co.uk"
#SHELL="/bin/bash"
#* * * * * /home/medadnew/HAB/MQTT_logger/run.sh
#
# Ensure the absolute path to this bash file is correct.
# may have to run `vim run.sh -c "set ff=unix" -c ":wq"` to convert the line encoding from DOS to Unix




#echo "running cron file"
if ! pgrep -f MQTT_logger.py > /dev/null
then
    echo "Mqtt Logger not running. firing up the logger"
    source /home/medadnew/virtualenv/HAB/3.6/bin/activate && cd /home/medadnew/HAB && nohup python MQTT_logger/MQTT_logger.py &
#else
    #echo "running"
fi




# for on the VPS
#!/bin/bash

#echo "running cron file"
#if ! pgrep -f MQTT_logger.py > /dev/null
#then
#    echo "Mqtt Logger not running. firing up the logger"
#    nohup python3 MQTT_logger.py &
#else
#    #echo "running"
#fi

