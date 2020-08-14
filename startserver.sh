#!/bin/bash

cd clientportal.gw
bin/run.sh root/conf.yaml &
cd ..
./autologin.sh
cliclick -m verbose -w 1 kd:cmd t:t ku:cmd
exit 0