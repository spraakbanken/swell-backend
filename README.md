## swell-backend

For the one-week pilot

### web api

Over https, or on secure websocket if preferred

#### set

Set the state for

`GET` or `POST`

Arguments: `{user: string, pass: string, state: any}`

Returns: `200 OK` hopefully

Setting the state also adds it to the history state with a timestamp.

#### get

`GET`

Arguments: `{user: string, pass: string}`

Returns: `any | null` the last state if there is one, otherwise `null`


### admin api

From the command-line on the server

#### adduser

    adduser USER PASS

Creates an user with username `USER` and password `PASS`

#### setuser

    setuser USER < STATE

Set the current state for user `USER` to `STATE` (from `stdin`)

Same as the web api's `set` (but does not require a password)

#### viewuser

    viewuser USER

Returns (on `stdout`):
```
{
    user: string,
    pass: string,
    state: any | null,
    history: {timestamp: DateLike, state: any}[]
}
```

### unit tests

```
$ adduser danr hunter2
$ viewuser danr
{"user": "danr", "password": "hunter2", "state": null, "history": []}
$ echo '[1,2]' | setuser danr
$ viewuser danr
{"user": "danr", "password": "hunter2", "state": [1,2], "history": [{"timestamp": "Thu Nov 16 08:41:32 CET 2017", "state": [1,2]}]}
$ echo '{"apa": "bepa"}' | setuser danr
$ viewuser danr
{"user": "danr", "password": "hunter2", "state": {"apa": "bepa"}, "history": [{"timestamp": "Thu Nov 16 08:41:32 CET 2017", "state": [1,2]}, {"timestamp": "Thu Nov 16 08:43:15 CET 2017", "state": {"apa": "bepa"}}]}
```

and similarly by using `set` and `get` instead of `setuser` and `viewuser` (but the web api `get` does not return the history, only current state)
