import os


class Config(object):
    """Paths and settings"""

    DB_PATH = os.path.abspath(os.path.join(__file__, "../../data"))
    DB_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    DB_FILE_EXT = "db"
    LOGDIR = os.path.abspath(os.path.join(__file__, "../../logs"))

    # Strings in data base:
    DB_USER = "user"
    DB_PASSWORD = "password"
    DB_STATE = "state"
    DB_DEFAULT_STATE = None
    DB_HIST = "history"
    DB_TIMESTAMP = "timestamp"
