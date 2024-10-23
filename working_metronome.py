#!/usr/bin/env python3
import subprocess
import sys
import time

bpm = int(sys.argv[1])
pause = 60/bpm

while True:
    time.sleep(pause)
    subprocess.Popen(["ogg123", "/usr/share/sounds/ubuntu/stereo/bell.ogg"])
