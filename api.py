import requests
import config
import base64

import database

session = requests.session()
session.headers["Authorization"] = f"Basic {base64.b64encode(config.apikey).decode('ascii')}"

def GetAllStreaming():
    req = session.get(config.apibase + f"vhosts/default/apps/{config.ovenapp}/streams")
    for stream in req.json()["response"]:

        user = database.GetAccount(stream)
        if user["hidden"] == 1:
            continue
        user["viewcount"] = GetViewers(user["username"])
        yield user


def IsPathActive(path):
    req = session.get(config.apibase + f"vhosts/default/apps/app/streams/{path}")
    return req.status_code == 200

def GetViewers(path):
    req = session.get(config.apibase+f"stats/current/vhosts/default/apps/{config.ovenapp}/streams/{path}")
    return req.json().get("response", {}).get("totalConnections", 0)
