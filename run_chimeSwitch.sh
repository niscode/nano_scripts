#!/bin/sh
### for Jetson-Nano

### for Linux

count=`ps -ef | grep sudo | grep -v grep | wc -l`
# echo $count

while true
do
  # sudoプロセスを監視
  if [ $count = 0 ]; then
    echo "[-]chimeSwitch Process Down  -----"
    echo "[+]chimeSwitch Process Start +++++"
    echo 'capf' | sudo -S python3 ~/nano_scripts/keyboard_ChimeSwitch.py CA000 ignis2-sock.ca-platform.org 11001 CA010

  else
    echo "[+]chimeSwitch Process OK    +++++"
    sleep 30
  fi
done

# echo 'capf' | sudo -S python3 ~/nano-scripts/keyboard_ChimeSwitch.py CA000 ignis2-sock.ca-platform.org 11001 CA010