#!/bin/bash

sudo apt install python3-pip &&
sudo apt install python3-venv &&
python3 -m venv ournft-env &&
source ournft-env/bin/activate &&
pip install -r requirements.txt && 
python3 ournft_site/generate_secret.py &&
python3 ournft_site/manage.py migrate --run-syncdb
