import os


class C(object):
    """Paths and settings"""

    Path = os.path.abspath(os.path.join(__file__, "../../data"))
    Logdir = os.path.abspath(os.path.join(__file__, "../../logs"))

    # Strings in data base:
    User = "user"
    Password = "password"
    State = "state"
    Statefile = "statefile"
    Repo = "repo"
    GCCountdown = "gccountdown"
    GCInterval = 25
    DefaultState = None
