#!/bin/bash
echo $(date)
echo "Start service check pppoe"
sudo /usr/bin/python3  ${pathcore}service/checkPPPoE.py >> /var/log/checkpppoe.log
echo "Start service init route"
sudo /etc/route_init.sh
echo "Restore iptables"
sudo iptables-restore < /etc/policy_init.sh
echo "Allow ip_foward"
sudo sysctl net.ipv4.ip_forward=1


