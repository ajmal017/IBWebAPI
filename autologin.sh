#!/bin/bash


open -a "Google Chrome" "https://localhost:5000/"
sleep 3.5
source .env
cliclick -w 10 t:$USERNAME kp:tab t:$PASSWORD kp:enter
sleep 2
exit 0