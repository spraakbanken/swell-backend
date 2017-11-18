#!/bin/bash
source venv/bin/activate
export FLASK_APP=cmd_api.py
user="usr-$(ls ../data | wc -l)"
echo $user
echo "{\"time\":\"$(date)\"}" | flask adduser $user hunter2 -
#flask viewuser $user
gunicorn index &
sleep 0.5
gu=$?
for i in $(seq 1 100); do
    msg='{"user":"'"$user"'","pw":"hunter2","state":"'"$(base64 -w 0 handlers.py)$(date +%s.%N)"'"}'
    curl 127.0.0.1:8000/set -d "$msg"
done
flask viewuser $user
msg='{"user":"'"$user"'","pw":"hunter2"}'
curl 127.0.0.1:8000/get -d "$msg"
kill $gu
