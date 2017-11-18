import logging
import os.path
import sys
import time
import stat
from config import C

# Set to None for logging to stdout
LOGDIR = C.Logdir

# Set debug level: DEBUG, INFO, WARNING, ERROR, CRITICAL
DEBUGLEVEL = logging.INFO

# Write to stdout or logfile?
DEBUG_TO_STDOUT = True if LOGDIR is None else False

# Format for log messages and date
LOGFMT = '%(asctime)-15s - %(levelname)s: %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'


if DEBUG_TO_STDOUT:
    logging.basicConfig(stream=sys.stdout, level=DEBUGLEVEL,
                        format=LOGFMT, datefmt=DATEFMT)
else:
    DEBUGFILE = os.path.join(LOGDIR, 'backend.log')
    # Create Logfile if it does not exist
    if not os.path.isfile(DEBUGFILE):
        with open(DEBUGFILE, "w") as f:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write("%s CREATED DEBUG FILE\n\n" % now)
        # Fix permissions
        os.chmod(DEBUGFILE, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH |
                 stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
    logging.basicConfig(filename=DEBUGFILE, level=DEBUGLEVEL,
                        format=LOGFMT, datefmt=DATEFMT)
