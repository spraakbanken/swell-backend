import sys
import logging
import json
from flask import Flask, Response, request
from db_communicate import update_state, save_userdb
from config import Config

app = Flask(__name__)
# CORS(app)  # enables CORS support on all routes
log = logging.getLogger('swell-backend.' + __name__)


@app.route('/')
@app.route('/hello')
def hello_world():
    log.info("Hello!")
    return Response(json.dumps({'success': True, 'message': 'Hello!'}), mimetype='application/json')


@app.route('/get', methods=['GET'])
def get_user():
    """Get a user's latest state if correct password is provided."""
    user = request.values.get('user', '')
    pw = request.values.get('pw', '')
    user_check = check_user(user, pw)

    if type(user_check) is dict:
        return Response(json.dumps(user_check.get("state", Config.DB_DEFAULT_STATE)), mimetype='application/json', status=200)
    else:
        return user_check


@app.route('/set', methods=['GET', 'POST'])
def set_state():
    """Update a user's state and history."""
    user = request.values.get('user', '')
    pw = request.values.get('pw', '')
    state = request.values.get('state', '')

    user_check = check_user(user, pw)

    # User check passed
    if type(user_check) is dict:
        try:
            userdb = update_state(user_check, user, state)
        except Exception as e:
            log.error("Could not update data base! %s", e)
            return json_error_response("Could not update data base! %s" % e)
        try:
            save_userdb(userdb, user, app.config["DataFiles"])
        except Exception as e:
            log.error("Could not save changes to data base! %s", e)
            return json_error_response("Could not save changes to data base! %s" % e)

        return Response(json.dumps({'success': True}), mimetype='application/json', status=200)

    # User check failed
    else:
        return user_check


###########################################################################
# Auxiliaries
###########################################################################

def check_user(user, pw):
    """
    Check if user exists and if password is valid.
    Return the user's data.
    """
    db = app.config["SwellDB"]
    userdata = db.get(user)

    if not userdata:
        log.error("Unknown user: %s", user)
        return json_error_response("Unknown user: %s" % user)
    elif userdata.get(Config.DB_PASSWORD) != pw:
        log.error("Invalid password!")
        return json_error_response("Invalid password!")
    return userdata


def json_error_response(msg, code=400):
    """Return json object with error message."""
    return Response(json.dumps({'success': False, 'error': {'message': msg}}), mimetype="application/json", status=code)
