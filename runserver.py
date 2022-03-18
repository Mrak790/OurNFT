from subprocess import run
from sys import platform

if platform.startswith('win32'):
    env_python = "ournft-env/Scripts/python"

elif platform.startswith('linux'):
    env_python = "ournft-env/bin/python3"

run([env_python, "ournft_site/manage.py", "makemigrations"])

run([env_python, "ournft_site/manage.py", "migrate", "--run-syncdb"])

run([env_python, "ournft_site/manage.py", "runserver"])