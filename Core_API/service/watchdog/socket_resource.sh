#!/bin/bash
out=$(ps ax |grep -v grep| grep ResourceService.py | wc -l)
if [ $out -eq '0' ]
then
  echo "Process not is running."
  /usr/bin/python3  ${pathcore}service/socket/ResourceService.py >> /var/log/bad/ResourceService.log
fi
