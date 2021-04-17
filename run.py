import os
import sys

from engine import info

def test(*args):
    info("Running unit tests...")
    os.system("python -m pytest tests/")

def run(*args):
    info("Starting up...")
    import songs.super_mario as super_mario
    super_mario.play()


do = run
args = []

if len(sys.argv) > 1:
    if sys.argv[1] == "test":
        do = test

if len(sys.argv) > 2:
    args = sys.argv[2:]

do(args)
