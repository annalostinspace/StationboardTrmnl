# -*- coding: utf-8 -*-
"""
Autor:   Florian Aliu
Datum:   %(date)s
E-Mail:  Florian.aliu@students.fhnw.ch

Datei:   infm_Datentypen_HS24.py ,%(filename)

Quelle:  ...
Zweck:   ...

Aufgabe: ...

Version: 0.[...]
"""

import json
import datetime
import pySBB
import requests


def getStationboard(station: str):
    entries = pySBB.get_stationboard(station, limit=8, transportations="train")

    departures = []

    for i in range(8):
        departure = {
            "train": entries[i].category + str(entries[i].number)
            if entries[i].number is not None else entries[i].category,
            "time": entries[i].stop.departure.strftime("%H:%M"),
            "to": entries[i].end,
            "platform": entries[i].stop.platform,
            "delay": str(entries[i].stop.delay) + " min"
            if entries[i].stop.delay >= 3 else ""
        }
        departures.append(departure)

    stationboard = {
        "merge_variables": {
            "station": station,
            "departures": departures
        }
    }

    return json.dumps(stationboard, ensure_ascii=False)


def uploadStationboard(stationboard):
    api_url = "https://usetrmnl.com/api/custom_plugins/"
    plugin_uuid = "7c0e640b-f0dd-418a-88df-f84723598ba8"
    headers = {"Content-Type": "application/json"}
    return requests.post(
        api_url + plugin_uuid,
        headers=headers,
        data=stationboard
    )

if __name__ == "__main__":
    response = uploadStationboard(getStationboard("Burgdorf"))
    now = datetime.datetime.now()
    print(now.strftime("%y.%m.%d %H:%M:%S ") + "Uploading Stationboard returned code: " + str(response.status_code))
