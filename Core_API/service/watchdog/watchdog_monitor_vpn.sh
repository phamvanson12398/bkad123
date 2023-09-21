#!/bin/bash
out=$(ps ax |grep -v grep| grep 'vpn_monitoring.py' | wc -l)
if [ $out -eq '0' ]
then
  echo "Process not is running."
  /usr/bin/python3  ${pathcore}service/vpn_monitoring.py 
fi




