import os
import sys
from string import Template

dir = os.path.dirname(os.path.realpath(__file__))
python_cmd = sys.executable
log_file = os.path.join(dir, 'log.txt')
script_file = os.path.join(dir, 'tweeter.py')

cron_job_template = Template('''
# This cron job does something very important
# Only posts in the most paranoid hours, from 2am to 5pm
# Every day of month, Every month, every day of week
12,35,58 2,3,4,5 * * * $cmd $file >> $log_file
''')

print(cron_job_template.substitute(cmd=python_cmd, file=script_file, log_file=log_file))
