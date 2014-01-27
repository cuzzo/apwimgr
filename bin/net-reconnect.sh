#! /usr/bin/env bash

# network-manager v. NetworkManger ; Ubuntu v. Fedora
#service network-manager restart
#iptables -F
echo $1 $2
iwconfig wlan0 essid "$1" key "$2"
