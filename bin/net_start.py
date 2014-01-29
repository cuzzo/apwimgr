#! /usr/bin/env python

import sys
import subprocess

import netutils as netutils


def main():
    interface = netutils.get_interface()
    last_network = netutils.get_last_network()
    netutils.connect(last_network.get("name"), interface)

if __name__ == "__main__":
    main()
