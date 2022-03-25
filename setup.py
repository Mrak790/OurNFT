from subprocess import run
from sys import platform

if platform.startswith('win32'):
    os_python = 'python'
    env_python = "ournft-env/Scripts/python"
    env_pip = "ournft-env/Scripts/pip"

elif platform.startswith('linux'):
    os_python = 'python3'
    env_python = "ournft-env/bin/python3"
    env_pip = "ournft-env/bin/pip"

run(["pip", "install", "virtualenv"])

run([os_python, "-m", "venv", "ournft-env"])

run([env_pip, "install", "-r", "requirements.txt"])

run([env_python, "ournft_site/generate_secret.py"])

run([env_python, "ournft_site/manage.py", "migrate", "--run-syncdb"])
