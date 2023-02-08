import sys
import subprocess


subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'click==7.1.2'])