import sys
import subprocess
import os

print('CWD: ' + os.getcwd())
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'click==7.1.2'])