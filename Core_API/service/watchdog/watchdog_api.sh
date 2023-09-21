#!/bin/bash
out=$(ps ax |grep -v grep| grep resources_api | wc -l)
if [ $out -eq '0' ]
then
  echo "Process not is running."
  sudo /usr/bin/python3 ${pathcore}resources_api.py  >> /var/log/bvg/resources_api.log
fi




