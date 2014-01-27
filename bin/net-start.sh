#! /usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONNECTION="$( dirname "$DIR" )/connection.dat"

$DIR/net-reconnect.sh $SSID $PASSWORD
