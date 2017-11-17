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

Arguments: `{user: string, password: string, state: any}`

Returns: `200 OK` hopefully

Sets the state for the given user and additionally adds it to the history with a timestamp.

#### get
Get the current state for a user via `GET`

Arguments: `{user: string, password: string}`

Returns: `any | null` the last state if there is one, otherwise `null`


## Admin API specifications

From the command-line on the server

#### adduser

    adduser --user USER --pw PASS

Creates an user with username `USER` and password `PASS`

#### setuser

    setuser --user USER --state STATE

Set the current state for user `USER` to `STATE` (from `stdin`)

Same as the web api's `set` (but does not require a password)

#### viewuser

    viewuser --user USER

Returns (on `stdout`):
```
{
    user: string,
    password: string,
    state: any | null,
    history: {timestamp: DateLike, state: any}[]
}
```

## unit tests

```
$ flask adduser --user danr --pw hunter2
$ flask viewuser --user danr
{"user": "danr", "password": "hunter2", "state": null, "history": []}
$ echo '[1,2]' | setuser danr
$ flask viewuser --user danr
{"user": "danr", "password": "hunter2", "state": [1,2], "history": [{"timestamp": "Thu Nov 16 08:41:32 CET 2017", "state": [1,2]}]}
$ echo '{"apa": "bepa"}' | setuser danr
$ flask viewuser --user danr
{"user": "danr", "password": "hunter2", "state": {"apa": "bepa"}, "history": [{"timestamp": "Thu Nov 16 08:41:32 CET 2017", "state": [1,2]}, {"timestamp": "Thu Nov 16 08:43:15 CET 2017", "state": {"apa": "bepa"}}]}
```

and similarly by using `set` and `get` instead of `setuser` and `viewuser` (but the web api `get` does not return the history, only current state)
