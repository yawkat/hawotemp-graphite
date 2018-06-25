#!/usr/bin/env python3

import re
import time
import traceback
import sys

import graphitesend

graphitesend.init(graphite_server=sys.argv[1], prefix="hawotemp", system_name="")


def telnet_get(host: str, port: int) -> str:
    import socket
    with socket.create_connection((host, port)) as s:
        return s.makefile().read()


while True:
    collected_data = {}
    # noinspection PyBroadException
    try:
        for sensor in ("east-temp", "west-temp"):
            lines = telnet_get(sensor + ".hawo.stw.uni-erlangen.de", 7338).splitlines()
            temp = float(re.match(r"(.+)C", lines[0]).group(1))
            humidity = float(re.match(r"(.+)% Humidity", lines[1]).group(1)) / 100.
            collected_data[sensor + ".temperature"] = temp
            collected_data[sensor + ".humidity"] = humidity
    except:
        traceback.print_exc()
    if len(collected_data) > 0:
        graphitesend.send_dict(collected_data)
    time.sleep(30)
