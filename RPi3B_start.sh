#!/bin/bash

# RPi3B+ Startup Script to allow user to activate FortiusAnt or 
# access RPi without FortiusAnt running

echo Starting RPi3B+ startup...
cd /home/pi/

# start python program with option to use FortiusAnt or normal RPi3B
# and get output from program. 
# If FortiusAnt is selected then start FortiusAnt

OUT=`python RPi3B_start.py`
echo $OUT
if [ "$OUT" == 'startFA' ]
then
	source FortiusANT.sh
fi

