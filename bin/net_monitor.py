#! /usr/bin/env python

import os
import subprocess
import time

import netutils
import net_server

# Globals
class Monitor(object):
    def __init__(self):
        settings = netutils.get_settings()

        self.ap = None
        self.mgr = None
        self.broadcasting = False
        self.interface = netutils.get_interface()
        self.ap_path = settings.get("ap_path")
        self.net_server_path = settings.get("net_server_path")

    def start_manager(self):
        if self.mgr is not None:
            try:
                self.mgr.kill()
            except:
                pass
        self.mgr = subprocess.Popen([self.net_server_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    def stop_manager(self):
        if self.mgr is not None and self.mgr.poll() is None:
            self.mgr.kill()
        self.mgr = None

    def start_access_point(self):
        if self.ap is not None:
            try:
                self.ap.kill()
                os.system("killall -9 dnsmasq")
            except:
                pass
        self.ap = subprocess.Popen([self.ap_path, self.interface, "eth0"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        self.broadcasting = True

    def stop_access_point(self):
        if self.ap is not None:
            if self.ap.poll() is None:
                self.ap.kill()
            try:
                os.system("killall -9 dnsmasq")
            except:
                pass
        self.ap = None
        self.broadcasting = False

    def connect_or_broadcast(self):
        if netutils.is_connected(2):
            if self.broadcasting:
                self.stop_manager()
                self.stop_access_point()
            return
        if self.broadcasting:
            return

        self.start_access_point()
        self.start_manager()


def main():
    monitor = Monitor()
    while True:
        try:
            monitor.connect_or_broadcast()
        except:
            pass
        time.sleep(60)

if __name__ == "__main__":
    main()
