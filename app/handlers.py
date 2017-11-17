import sys
import logging
import json
from flask import Flask, Response, request
from db_communicate import update_state, save_userdb
from config import Config

app = Flask(__name__)
# CORS(app)  # enables CORS support on all routes
log = logging.getLogger('swell-backend.' + __name__)


@app.route('/hello')
def hello_world():
    log.info("Hello!")
    return Response(json.dumps("{'success': true, 'message': 'Hello!'}"), mimetype='application/json')



@app.route('/get', methods=['GET'])
def get_user():
    """Get a user's latest state if correct password is provided."""
    user = request.values.get('user', '')
    pw = request.values.get('pass', '')
    user_check = check_user(user, pw)

    if type(user_check) is dict:
        return Response(json.dumps(user_check.get("state", "null")), mimetype='application/json', status=200)
    else:
        return user_check


@app.route('/set', methods=['GET', 'POST'])
def set_state():
    """Update a user's state and history."""
    user = request.values.get('user', '')
    pw = request.values.get('pass', '')
    state = request.values.get('state', '')

    user_check = check_user(user, pw)

    if type(user_check) is dict:
        try:
            userdb = update_state(user_check, user, state)
        except:
            return json_error_response("Could not update data base! %s" % sys.exc_info()[0])
        try:
            save_userdb(userdb, user, app.config["DataFiles"])
        except:
            return json_error_response("Could not save changes to data base! %s" % sys.exc_info()[0])

    return Response(json.dumps("{'success': true}"), mimetype='application/json', status=200)


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
        return json_error_response("Unknown user: %s" % user)
    elif userdata.get(Config.DB_PASSWORD) != pw:
        return json_error_response("Invalid password!")
    return userdata


def json_error_response(msg, code=400):
    """Return json object with error message."""
    return Response(json.dumps("{'success': false, 'error': {'message': %s}}" % msg), mimetype="application/json", status=code)
