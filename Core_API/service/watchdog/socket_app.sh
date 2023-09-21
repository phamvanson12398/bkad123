#!/bin/bash
out=$(ps ax |grep -v grep| grep socketapp.py | wc -l)
if [ $out -eq '0' ]
then
  echo "Process not is running."
  /usr/bin/python3  ${pathcore}service/socket/socketapp.py   >> /var/log/bad/socketapp.log 
fi




