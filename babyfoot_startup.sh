#!/bin/sh

source ../iot-babyfoot/bin/activate

python3 score_fetcher/comm.py

python3 web_interface/app.py 

DISPLAY=:0 chromium-browser --high-dpi-support=1 --force-device-scale-factor=0.5 --start-fullscreen http://localhost:5000

