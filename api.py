import requests
import config
import base64
from hashlib import sha256

import database


def AddPath(name, password):
    req = requests.post(config.apibase + f"config/paths/add/{name}",
                  json={
                      "publishUser": name,
                      "publishPass": password
                  })
    return req.status_code == 200


def GetAllStreaming():
    req = requests.get(config.apibase + f"paths/list")
    for path, info in req.json()["items"].items():
        if info["sourceReady"]:
            user = database.GetAccount(path)
            if user["hidden"] == 1:
                continue
            yield path, user, info


def IsPathActive(path):
    req = requests.get(f"http://localhost:8888/{path}/")
    return req.status_code == 200