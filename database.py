import sqlite3
import config
import random
import base64
import api
from flask import g
from passlib.hash import pbkdf2_sha256

def MakeKey():
    return base64.b32encode(random.getrandbits(256).to_bytes(32, "big")).strip(b"=").decode("utf8")

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.db, isolation_level=None)
        db.row_factory = make_dicts
    return db

def Initialize():
    _local = sqlite3.connect(config.db)
    _local.row_factory = make_dicts
    _local.execute("PRAGMA journal_mode = WAL;")
    _local.execute("CREATE TABLE IF NOT EXISTS users (`username` STRING, `password` STRING, `title` STRING, `key` STRING, `hidden` INTEGER)")
    _local.execute("CREATE TABLE IF NOT EXISTS invites (`token` TEXT)")


    for row in _local.execute("SELECT * FROM users"):
        api.AddPath(row["username"], row["key"])

def GetAccount(username):
    q = get_db().execute("SELECT * FROM `users` WHERE username LIKE ?", (username, ))
    if not q:
        return None
    else:
        fetch = q.fetchone()
        return fetch

def CreateAccount(username, password):
    key = MakeKey()
    get_db().execute("INSERT INTO `users` VALUES (?, ?, ?, ?, ?)",
                           (username,
                            pbkdf2_sha256.hash(password),
                            f"{username}'s stream",
                            key,
                            0))
    api.AddPath(username, key)

def UpdateAccount(username, title, visibility):
    get_db().execute("UPDATE `users` SET `title` = ?, `hidden` = ? WHERE username = ?",
                     (
                         title, visibility, username
                     ))

def HasToken(token):
    q = get_db().execute("SELECT * FROM invites WHERE token = ?",
                     (
                         token,
                     ))
    return q.fetchone()

def RemoveToken(token):
    get_db().execute("DELETE FROM `invites` WHERE `token` = ?",
                     (
                         token,
                     ))