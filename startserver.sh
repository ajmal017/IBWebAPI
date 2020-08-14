#!/bin/bash

cd clientportal.gw
bin/run.sh root/conf.yaml &
cd ..
./autologin.sh
exit 0