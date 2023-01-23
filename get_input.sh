#!/bin/sh

INPUT_DEVICE=`pactl list short sources | grep Yamaha | grep input | awk '{print $2}'`
echo $INPUT_DEVICE
pactl set-default-source $INPUT_DEVICE