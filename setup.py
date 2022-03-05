from subprocess import run

run(["pip", "install", "virtualenv"])

run(["python", "-m", "venv", "ournft-env"])

env_python = "ournft-env\\Scripts\\python"
env_pip = "ournft-env\\Scripts\\pip"

run([env_pip, "install", "-r", "requirements.txt"])

run([env_python, "ournft_site/generate_secret.py"])

run([env_python, "ournft_site/manage.py", "migrate"])
