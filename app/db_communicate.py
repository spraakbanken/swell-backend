import logging
import sys
import os
import json
import time
import datetime
from config import Config

log = logging.getLogger('swell-backend.' + __name__)


def load_db():
    """Read all the json data in Config.DB_PATH and save it as a dictionary."""
    log.info("Resuming the data base")
    swellDB = {}
    filedict = {}

    for dbfile in os.listdir(Config.DB_PATH):
        fpath = os.path.join(Config.DB_PATH, dbfile)
        if os.path.isfile(fpath):
            with open(fpath, "r") as f:
                contents = json.load(f)
                user = contents.get(Config.DB_USER)
                swellDB[user] = contents
                filedict[user] = fpath
    return swellDB, filedict


def update_state(userdb, user, state):
    """Update the current state of user and save it to their history."""
    history = userdb.get("history", [])

    ts = get_timestamp()
    history.append({Config.DB_TIMESTAMP: ts, Config.DB_STATE: state})
    userdb[Config.DB_STATE] = state
    return userdb


def get_timestamp():
    """Creates a time stamp in the specified format."""
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime(Config.DB_DATEFORMAT)


def save_userdb(userdb, user, filedict):
    """Save one user's data base to a file."""
    user_file = filedict.get(user, os.path.join(Config.DB_PATH, "%s.%s" % (user, Config.DB_FILE_EXT)))
    with open(user_file, "w") as f:
        json.dump(userdb, f)


def add_user(user, pw, db, filedict):
    """Add a new user to the data base."""
    if not db.get(user):
        db[user] = {}
        db[user][Config.DB_USER] = user
        db[user][Config.DB_PASSWORD] = pw
        db[user][Config.DB_STATE] = "null"
        db[user][Config.DB_HIST] = []

        try:
            save_userdb(db[user], user, filedict)
        except:
            "Could not save changes to database! %s" % sys.exc_info()[0]

    else:
        raise "User '%s' already exists!" % user
