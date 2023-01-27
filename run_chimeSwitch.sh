#!/bin/sh
### for Jetson

count=`ps -ef | grep sudo | grep -v grep | wc -l`
exp=1

while true
do
  echo "Please wait for 10 sec ..."
  sleep 10
  # sudoプロセスを監視
  if [ $count = 0 ]; then
    echo "[-]chimeSwitch Process Down  -----"
    echo "[+]chimeSwitch Process Start +++++"
    echo 'capf' | sudo -S python3 ~/nano_scripts/keyboard_ChimeSwitch.py CA000 ignis2-sock.ca-platform.org 11001 CA010 >> chime.log

    # keyboard_ChimeSwitch.pyの実行が何らかのエラーによって止まったとき
    echo $((exp ++))

  else
    if [ $exp = 2 ] || [ $((exp / 10)) = 0 ]; then
      # 初回起動の停止時と100秒に1回、プロセスを強制キル
      pid=`ps -ax | grep sudo | grep keyboard | awk '{ print $1 }'`
      echo 'capf' | sudo -S kill -9 $pid``
    else
      echo "[+]chimeSwitch Process OK    +++++"
      sleep 10
    fi
    echo $((exp ++))
  fi

  # else
  #   echo "[+]chimeSwitch Process OK    +++++"
  #   sleep 10
  # fi
done