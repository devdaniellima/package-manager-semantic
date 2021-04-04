import os, subprocess
from env import *

def midsiServerIsRunning():
  subprocess.call(['tilix', '-e', 'python3 midsi-service.py'], cwd= str(MIDSI_PATH) + '/service')