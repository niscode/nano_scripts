#!/bin/sh
cd ~/
ln -s nano_scripts/login_capf.sh
ln -s nano_scripts/launch_client.sh
ln -s nano_scripts/run_chimeSwitch.sh
ln -s nano_scripts/gitpull_scripts.sh
ln -s nano_scripts/get_output.sh
ln -s nano_scripts/get_input.sh

# move autostart config files
cp ~/nano_scripts/autostart/* ~/.config/autostart/