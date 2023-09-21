#!/bin/bash
echo date
echo "Reconnecting PPPoE"
/usr/bin/python3  ${pathcore}service/checkPPPoE.py > /var/log/checkpppoe.log





