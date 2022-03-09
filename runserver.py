from subprocess import run

env_python = "ournft-env\\Scripts\\python"

run([env_python, "ournft_site/manage.py", "makemigrations"])

run([env_python, "ournft_site/manage.py", "migrate", "--run-syncdb"])

run([env_python, "ournft_site/manage.py", "runserver"])