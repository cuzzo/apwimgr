#! /usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MAXPLOSS=10

start_ap() {
	echo 'AP_WAIT="1"' > net.dat
	/etc/init.d/networking restart
	iptables -F
	ap.sh wlan0 etho0
}

is_connected() {
	ploss=101
	ploss=$(ping -q -w3 google.com | grep -o "[0-9]*%" | tr -d %) \
		> /dev/null 2>&1

	if [ "$ploss" -gt "$MAXPLOSS" ]; then
		return 0
	fi
	return 1
}

source $( dirname "$DIR" )/net.dat

if is_connected ; then : else
	$DIR/net-reconnect.sh
	if is_connected ; then : else
		if [ "$AP_WAIT" -eq "0" ] ; then
			start_ap
		fi
	fi
fi
