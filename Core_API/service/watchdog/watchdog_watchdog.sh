#!/bin/bash
out=$(ps ax |grep -v grep| grep 'run_watchdog.py' | wc -l)
if [ $out -eq '0' ]
then
  echo "Process not is running."
  /usr/bin/python3  ${pathcore}service/watchdog/run_watchdog.py  >> /var/log/bvg/watchdog.log 
fi




