#!/bin/bash

cd clientportal.gw
bin/run.sh root/conf.yaml & echo $!
cd ..
./autologin.sh
exit 0