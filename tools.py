#!./venv/bin/python3 python3
from documents import development_log_manager
import os
import sys

if __name__ == "__main__":
    try:
        if sys.argv[1] == "log":
            development_log_manager.record_log()
    except ImportError as exc:
        raise ImportError(
            "Couldn't find the command '{0}'".format(sys.argv[1])
        ) from exc


"""
To create a new executable "chmod +x myfile.py"
"""