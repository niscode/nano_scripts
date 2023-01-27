#!/bin/sh
### for Jetson

count=`ps -ef | grep sudo | grep -v grep | wc -l`
# echo $count
is_work=true

while true
do
  # 起動〜 10秒後に実行
  echo "Please wait for 10 sec ..."
  sleep 10
  # sudoプロセスを監視
  if "$is_work" && [ $count = 0 ]; then
    echo "[-]chimeSwitch Process Down  -----"
    echo "[+]chimeSwitch Process Start +++++"
    echo 'capf' | sudo -S python3 ~/nano_scripts/keyboard_ChimeSwitch.py CA000 ignis2-sock.ca-platform.org 11001 CA010 >> chime.log

    # keyboard_ChimeSwitch.pyの実行が何らかのエラーによって止まったとき
    echo "keyboad_ChimeSwitchが終了したみたい"
    is_work=false
    count=`ps -ef | grep sudo | grep -v grep | wc -l`
  else
    if ! "$is_work" && [ $count = 1 ]; then
      pid=`ps -ax | grep sudo | grep keyboard | awk '{ print $1 }'`
      echo 'capf' | sudo -S kill -9 $pid
      echo "プロセスを強制キルした。10秒後復帰に入る。"
    fi
    is_work=true
  fi
done