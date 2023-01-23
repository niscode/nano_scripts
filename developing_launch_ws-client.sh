#!/bin/sh

### before you start this script, you have to install the following,
#
#   sudo apt install python3-pip
#   pip3 install websocket-client
#   pip3 install rel
#
### install list - end

# ignis2 env
python3 ~/scripts/ws-client.py "https://ignis2.ca-platform.org/api/login" "CA001" "CA001" "wss://ignis2-websocket.ca-platform.org" "localhost" "1890" "10.186.42.60" "5001"
# python3 ~/scripts/ws-client.py "https://ignis2.ca-platform.org/api/login" "CA001" "CA001" "wss://ignis2-websocket.ca-platform.org" "localhost" "1890" "192.168.100.88" "5001"
