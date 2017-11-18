import sys
import logging
import json
from flask_cors import CORS
from flask import Flask, Response, request
import db_communicate as DB
from config import C

app = Flask(__name__)
CORS(app)  # enables CORS support on all routes
log = logging.getLogger('swell-backend.' + __name__)


@app.route('/')
@app.route('/hello')
def hello_world():
    log.info("Hello!")
    return Response(json.dumps({'success': True, 'message': 'Hello!'}), mimetype='application/json')


@app.route('/get', methods=['POST'])
def get_user():
    """Get a user's latest state if correct password is provided."""

    try:
        data = json.loads(request.get_data().decode())
        user = data.get('user')
        pw = data.get('pw')
    except Exception as e:
        log.error("Bad POST body", e)
        return json_error_response("Bad POST body %s" % e)

    user_check = DB.check_user(user, pw, app.config["SwellDB"])

    if type(user_check) is dict:
        return Response(
            json.dumps(user_check.get(C.State, C.DefaultState)),
            mimetype='application/json',
            status=200)
    elif type(user_check) is str:
        return json_error_response(user_check)
    else:
        return json_error_response('user_check fail')



@app.route('/set', methods=['POST'])
def set_state():
    """Update a user's state and history."""

    try:
        data = json.loads(request.get_data().decode())
        user = data.get('user')
        pw = data.get('pw')
        state = data.get('state')
    except Exception as e:
        return json_error_response("Bad POST body %s" % e)

    user_check = DB.check_user(user, pw, app.config["SwellDB"])

    if type(user_check) is dict:
        try:
            DB.update_state(user, state, app.config["SwellDB"])
            return Response(json.dumps({'success': True}), mimetype='application/json', status=200)
        except Exception as e:
            return json_error_response("Could not save changes to data base! %s" % e)
    elif type(user_check) is str:
        return json_error_response(user_check)
    else:
        return json_error_response('user_check fail')

###########################################################################
# Auxiliaries
###########################################################################

def json_error_response(msg, code=400):
    """Return json object with error message."""
    log.error(msg)
    return Response(
        json.dumps({
            'success': False,
            'error': {'message': msg}
        }),
        mimetype="application/json", status=code)
