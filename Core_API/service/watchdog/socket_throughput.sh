#!/bin/bash
out=$(ps ax |grep -v grep| grep ThroughputService.py | wc -l)
if [ $out -eq '0' ]
then
  echo "Process not is running."
  /usr/bin/python3  ${pathcore}service/socket/ThroughputService.py >> /var/log/bad/ThroughputService.log
fi




