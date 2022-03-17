from subprocess import run
from sys import platform
if platform.startswith('win32'):
    os_python = "python"
elif platform.startswith('linux'):
    os_python = "python3"

env_python = "ournft-env\\Scripts\\" + os_python

run([env_python, "ournft_site/manage.py", "makemigrations"])

run([env_python, "ournft_site/manage.py", "migrate", "--run-syncdb"])

run([env_python, "ournft_site/manage.py", "runserver"])