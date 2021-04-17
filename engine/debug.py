"""
Debug/logging interface. This file will automatically parse command line
elements when loaded into a module to determine the correct log level.
"""

import sys

from datetime import datetime
from enum import IntEnum

class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

    def __repr__(self):
        return self.name

LOG_LEVEL = LogLevel.DEBUG
"""
The log level. Defaults to DEBUG unless the log level is provided as a command
line argument.
"""

def log(level: LogLevel, msg: str):
    """
    Log a message at the specified log level (engine.LogLevel).

    Args:
        level: The log level.
        msg: The message to log.
    """
    if level >= LOG_LEVEL:
        now = datetime.now()
        print(f"{now.isoformat()} [{repr(level)}]: " + msg)

def debug(msg: str):
    """
    Log a message at the debug level. Will not print if LOG_LEVEL > DEBUG.

    Args:
        msg: The message to log.
    """
    log(LogLevel.DEBUG, msg)

def info(msg: str):
    """
    Log a message at the info level. Will not print if LOG_LEVEL > INFO.

    Args:
        msg: The message to log.
    """
    log(LogLevel.INFO, msg)

def warn(msg: str):
    """
    Log a message at the warn level. Will not print if LOG_LEVEL > WARN.

    Args:
        msg: The message to log.
    """
    log(LogLevel.WARN, msg)

def error(msg: str):
    """
    Always print errors.

    Args:
        msg: The message to log.
    """
    print(msg)

# Pick the log level from command line arguments. If multiple are specified,
# this will choose the last one specified.
for arg in sys.argv:
    if arg == "--debug":
        LOG_LEVEL = LogLevel.DEBUG
    elif arg == "--info":
        LOG_LEVEL = LogLevel.INFO
    elif arg == "--warn":
        LOG_LEVEL = LogLevel.WARN
    elif arg == "--error":
        LOG_LEVEL = LogLevel.ERROR

info(f"Logging at: {str(LOG_LEVEL)}")