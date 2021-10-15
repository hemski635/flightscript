#!/bin/sh

raspivid -o vid.h264 -t 180000 & \
        ./flightscript.py & \
        echo $(date) >> ./GPSLOG.log & \
        sudo cat /dev/ttyS0 >> ./GPSLOG.log
