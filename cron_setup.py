import os
import sys
from distutils.spawn import find_executable
from string import Template

dir = os.path.dirname(os.path.realpath(__file__))
python_cmd = sys.executable
update_script = os.path.join(dir, 'update.sh')
log_file = os.path.join(dir, 'tweets.log')
tweet_script = os.path.join(dir, 'tweeter.py')

cron_job_template = Template('''
# Only posts in the most paranoid hours, from 2am to 5pm
# Every day of month, Every month, every day of week
12,35,58 2,3,4,5 * * * $python_cmd $script >> $log_file

# Clear the log once a month
0 0 1 * * $rm $log_file

# Update daily
0 0 * * * $bash $update_script
''')

file_text = cron_job_template.substitute(
    python_cmd=python_cmd,
    script=tweet_script,
    log_file=log_file,
    update_script=update_script,
    rm=find_executable('rm'),
    bash=find_executable('bash')
)
print(file_text)
