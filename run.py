import importlib
import os
import sys

from engine import info

def test(*args):
    info("Running unit tests...")

    path = "tests/"
    if len(args) > 0:
        path = args[0]
    os.system(f"python -m pytest {path}")

def run(*args):
    info("Starting up...")

    # Default to super mario.
    module_name = "super_mario"
    if len(args) > 0:
        module_name = args[0]

    module_name = "songs." + module_name
    module = importlib.import_module(module_name)
    module.play()

do = run
args_to_skip = 1

if len(sys.argv) > 1:
    if sys.argv[1] == "test":
        do = test
        args_to_skip = 2

do(*sys.argv[args_to_skip:])
