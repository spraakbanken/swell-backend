import os
import sys
import logging

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
if THIS_DIR not in sys.path:
    sys.path.append(THIS_DIR)

# Setup logging
import logger
log = logging.getLogger('swell-backend')
log.info("Restarted index.py")

# Load data base
from db_communicate import load_db
SwellDB, DataFiles = load_db()


def application(env, resp):
    """
    Wrapper for the flask application.
    It is best run with gunicorn.
    All routes are specified in handlers.py
    """

    try:
        from handlers import app as real_app
        env['SCRIPT_NAME'] = ''

        # Save data base in app
        real_app.config["SwellDB"] = SwellDB
        real_app.config["DataFiles"] = DataFiles

        return real_app(env, resp)

    except:
        log.exception("Error while running application.")
        return ["Error while running application."]


if __name__ == "__main__":
    """
    For local testing. Run with gunicorn otherwise since
    waitress does not support continuous response streaming.
    """
    from waitress import serve
    serve(application, host='0.0.0.0', port=55000)
