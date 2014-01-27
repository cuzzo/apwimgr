#! /usr/bin/env python

import os
import inspect
import subprocess

from bottle import Bottle, run, request, static_file, SimpleTemplate
from iw_parse.iw_parse import get_parsed_cells

app = Bottle()

wireless_interface = "wlan0"
base_tpl_path = "tpl/base.html"

def get_base_path():
    script_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    base_path = os.path.dirname(os.path.dirname(script_path))
    return base_path

def get_template(rel_path):
    plain_text = open(os.path.join(get_base_path(), rel_path), "r").read()
    return SimpleTemplate(plain_text)

def is_connected():
    host = "google.com"
    ping = subprocess.Popen(
        ["ping", "-c", "4", host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = ping.communicate()
    if error:
        return False
    return True

def get_networks():
    iwlist = subprocess.Popen(
        ["iwlist", wireless_interface, "scan"],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

    out, error = iwlist.communicate()
    return get_parsed_cells(out.split("\n"))

def get_network_by_ssid(network_list, ssid):
    for network in network_list:
        if network.get("Name", "") == ssid:
            return network
    return {}

def get_ssid_select(network_list):
    select = "<select name=\"ssid\">"
    for network in network_list:
        select += "<option value=\"{0}\">{0}</option>" \
                    .format(network.get("Name", "Unknown"))
    select += "</select>"
    return select


@app.get("/")
def index():
    ssid_select = get_ssid_select(networks)
    body = """
            <h1>AKU</h1>
            <form action="/connect" method="post">
                SSID: {0}
                Password: <input name="password" type="password" />
                <input value="Connect" type="submit" />
            </form>
        """.format(ssid_select)
    return base_tpl.render(title="AP Network Manager", body=body)

@app.post("/connect")
def connect():
    ssid = request.forms.get("ssid")
    password = request.forms.get("password")
    network = get_network_by_ssid(networks, ssid)
    encryption = network.get("Encryption", "WEP")

    with open(os.path.join(get_base_path(), "net.dat"), "wb") as f:
        f.write("AP_WAIT=\"0\"")

    #nrpath = os.path.join(get_base_path(), "bin", "net-reconnect.sh")
    #subprocess.call([nrpath, ssid, password], shell=True)

    if is_connected():
        with open(os.path.join(get_base_path(), "connection.dat"), "wb") as f:
            f.write("SSID={0}\nPASSWORD={1}\nENCRYPTION={2}" \
                    .format(ssid, password, encryption)
            )

    body = """
            <h1>AKU</h1>
            <p>Thank you! I am connecting now.</p>
        """
    return base_tpl.render(title="AP Network Manager", body=body)

@app.route("/static/<filepath:path>")
def server_static(filepath):
    net_path = os.path.join(get_base_path(), "net_server")
    return static_file(filepath, root=net_path)


base_tpl = get_template(base_tpl_path)
networks = get_networks()

run(app, host="localhost", port="8088")
