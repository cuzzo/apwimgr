import subprocess
import datetime

import iw_parse.iw_parse as iw_parse


def is_connected(count):
    host = "google.com"
    ping = subprocess.Popen(
        ["ping", "-c", str(count), host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = ping.communicate()
    if error:
        return False
    return True

def get_networks(interface):
    iwlist = subprocess.Popen(
        ["iwlist", interface, "scan"],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = iwlist.communicate()
    if error:
        return []
    return iw_parse.get_parsed_cells(out.split("\n"))

def get_network_by_ssid(network_list, ssid):
    for network in network_list:
        if network.get("Name", "") == ssid:
            return network
    return {}

def get_last_network():
    nmcli = subprocess.Popen(
        ["nmcli", "-t", "--fields", "NAME,TYPE,TIMESTAMP-REAL", "c", "list"],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = nmcli.communicate()
    out = filter(None, out.split("\n"))
    connected_network_list = nmcliclist.get_parsed_cells(out)
    if len(connected_network_list) == 0:
        return {}
    return connected_network_list[0]

def get_parsed_cells(data):
    cells=[]
    for line in data:
        name, connection_type, time_str = line.split(":", 2)
        if connection_type.find("ethernet") != -1 or \
            connection_type.find("wireless") == -1:
            continue

        try:
            time = datetime.datetime.strptime(time_str[:15], "%a %d %b %Y")
        except:
            time = datetime.datetime(1500, 12, 21) # old
        cells.append({"name": name, "time": time})

    cells = sorted(cells, key=lambda  k: k["time"])
    cells.reverse()
    return cells

def get_last_network():
    nmcli = subprocess.Popen(
        ["nmcli", "-t", "--fields", "NAME,TYPE,TIMESTAMP-REAL", "c", "list"],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = nmcli.communicate()
    out = filter(None, out.split("\n"))
    connected_network_list = get_parsed_cells(out)
    if len(connected_network_list) == 0:
        return {}
    return connected_network_list[0]

def get_interface():
    iwconfig = subprocess.Popen("iwconfig",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
    out, error = iwconfig.communicate()

    out = out.split("\n")
    for line in out:
        if line == "":
            continue
        if line.find("no wireless extensions") != -1:
            continue
        return line.split(" ", 1)[0]

def register_connection(cc_path, ssid, password, encryption):
    if encryption != "WEP":
        encryption = "WPA"
    encryption = encryption.lower()

    cc = subprocess.Popen(
        [cc_path, "wifi", "-S", encryption, "-K", password, ssid],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = cc.communicate()
    return not error

def connect(ssid, interface):
    nmcli = subprocess.Popen(
        ["nmcli", "-p", "con", "up", "id", ssid, "iface",
            interface, "--timeout", "10"],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = nmcli.communicate()
    return not error


def get_settings():
    ConfigParser = __import__("ConfigParser")
    cp = ConfigParser.ConfigParser()
    cp.readfp(open("/etc/apwimgr/apwimgr.conf"))
    items = cp.items("base")

    setting_dict = {}
    for item in items:
        setting_dict[item[0]] = item[1]
    return setting_dict
