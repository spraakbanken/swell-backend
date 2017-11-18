# swell-backend

For the one-week pilot

## Setup

* Create python 3 virtual environment (preferably from within app directory):

    `python3 -m venv venv`

* Activate virtualenv:

    `source venv/bin/activate`

* Upgrade pip (sometimes necessary) and install requirements:

    `pip install --upgrade pip`

    `pip install -r requirements.txt`

* Create logs and data directory

* Adapt configuration in config.py

* Run web API:

`PATH_TO_BACKEND/app/venv/bin/gunicorn -b 0.0.0.0:55000 index --chdir PATH_TO_BACKEND/app`

* Run command-line API (virtualenv must be activated):

    `export FLASK_APP=cmd_api.py`


## Web API specifications

Over https, or on secure websocket if preferred

#### set

Set the state for a user via `GET` or `POST`

Arguments: `{user: string, pass: string, state: any}`

Returns: `200 OK` hopefully

Example: `/set?user=danr&pass=hunter2&state={"apa": "bepa"}`

Sets the state for the given user and additionally adds it to the history with a timestamp.

#### get
Get the current state for a user via `GET`

Arguments: `{user: string, pass: string}`

Example: `/get?user=danr&pass=hunter2`

Returns: `any | null` the last state if there is one, otherwise `null`


## Admin API specifications

From the command-line on the server

#### adduser

    adduser USER PASS FILENAME

Creates an user with username `USER` and password `PASS` with initial state the json state in `FILENAME` (`-` for `stdin`)

#### setuser

    setuser USER FILENAME

Set the current state for user `USER` to the json state in `FILENAME` (`-` for `stdin`)

Same as the web api's `set` (but does not require a password)

#### viewuser

    viewuser USER

Writes the state (on `stdout`)

## unit tests

```
$ echo null | flask adduser danr hunter2 -
$ flask viewuser danr
null
$ echo '[1,2]' | flask setuser danr -
$ flask viewuser danr
[1,2]
$ echo '{"apa": "bepa"}' | flask setuser danr -
$ flask viewuser danr
{"apa": "bepa"}
$ (cd ../data/danr; git log --pretty=oneline) | wc -l
3
```

and similarly by using `set` and `get` instead of `setuser` and `viewuser` (but the web api `get` does not return the history, only current state)
