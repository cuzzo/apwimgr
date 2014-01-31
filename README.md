AP Network Manager
------------------

Manage your wireless network from an access point. It's the 21st century.

Dependencies
------------

* NetworkManager
* dnsmasq
* hostapd

Installation
------------

After you have installed the dependencies, run `./install.sh`.

Setup
-----

### hostapd.conf

Change your `/etc/hostapd/hostapd.conf` file to something like:

```
interface=<INTERFACE-NAME>
driver=nl80211
hw_mode=g
ssid=<MY-SSID/NETWORK-NAME>
channel=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
wpa_passphrase=<MY-PASSWWORD>
```

* Replace `<INTERFACE-NAME>` with your interface name. You can use `netutils.get_interface()` to get your interface name. It is usually something like `wlan0`.
* Replace `<MY-SSID/NETWORK-NAME>` with the desired name for your wireless network.
* Replace `<MY-PASSWORD>` with the desired password for your wireless network.

### dnsmasq.conf

Change your `/etc/dnsmasq.conf` file to something like:

```
no-resolv
interface=<INTERFACE-NAME>
dhcp-range=10.0.0.3,10.0.0.10,12h
server=8.8.8.8
server=8.8.4.4
```

License
-------

AP Network Manger is free--as in BSD. Hack your heart out, hackers.
