#/bin/bash
source venv/bin/activate
pip install -r requirements.txt

uwsgi --reload media/logs/uwsgi.pid