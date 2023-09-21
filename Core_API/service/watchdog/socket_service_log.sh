#!/bin/bash
out=$(ps ax |grep -v grep| grep service_log.py | wc -l)
if [ $out -eq '0' ]
then
  echo "Process not is running."
  /usr/bin/python3  ${pathcore}service/socket/service_log.py >> /var/log/bad/service_log.log
fi




