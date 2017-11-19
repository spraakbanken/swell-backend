import logging
import os
import json
import time
import datetime
from config import C
import git

log = logging.getLogger('swell-backend.' + __name__)


def user_files(fpath):
    return {
        C.User: os.path.join(fpath, C.User),
        C.Password: os.path.join(fpath, C.Password),
        C.Statefile: os.path.join(fpath, C.State),
    }


def load_user(fpath, DB, load_state=True):
    files = user_files(fpath)
    user = open(files[C.User]).read()
    pw = open(files[C.Password]).read()
    DB[user] = {
        C.Password: pw,
        C.Statefile: files[C.Statefile],
        C.Repo: git.Repo(fpath),
        C.GCCountdown: C.GCInterval
    }
    if load_state:
        state_text = open(files[C.Statefile]).read()
        state = json.loads(state_text)
        DB[user][C.State] = state,


def load_db():
    """Read all the json data in C.Path and save it as a dictionary."""
    log.info("Resuming the data base")
    DB = {}

    for dbfile in os.listdir(C.Path):
        fpath = os.path.join(C.Path, dbfile)
        if os.path.isdir(fpath):
            try:
                load_user(fpath, DB)
            except Exception as e:
                log.error("Non-conformant user directory %s %s" % (fpath, e))

    return DB


def update_state(user, state, DB):
    """Update the current state of user and save it to their history."""
    #history = userdb.get("history", [])

    #ts = get_timestamp()
    #history.append({C.Timestamp: ts, C.State: state})

    db = DB[user]
    db[C.State] = state
    json.dump(state, open(db[C.Statefile], 'w'), indent=2)
    repo = db[C.Repo]
    index = repo.index
    index.add([db[C.Statefile]])
    index.commit('update_state')
    db[C.GCCountdown] -= 1
    if db[C.GCCountdown] <= 0:
        db[C.GCCountdown] = C.GCInterval
        print('running gc')
        repo.git.gc()
        print('gc finished')


def check_user(user, pw, DB):
    """
    Check if user exists and if password is valid.
    Return the user's data as a dict or a string with an error message.
    """
    userdata = DB.get(user)

    if not userdata:
        log.error("Unknown user: %s", user)
        return "Unknown user: %s" % user
    elif userdata.get(C.Password) != pw:
        log.error("Invalid password!")
        return "Invalid password!"
    return userdata


def add_user(user, pw, init_state, DB):
    """Add a new user to the data base."""
    if not DB.get(user):
        fpath = os.path.join(C.Path, user)
        repo = git.Repo.init(fpath)

        files = user_files(fpath)

        open(files[C.User], 'w').write(user)
        open(files[C.Password], 'w').write(pw)

        repo.index.add([files[C.User], files[C.Password]])
        repo.index.commit("add_user")

        load_user(fpath, DB, load_state=False)

        update_state(user, json.loads(init_state), DB)
    else:
        raise Exception("User '%s' already exists!" % user)
