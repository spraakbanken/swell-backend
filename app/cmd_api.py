import click
import json
import sys
from flask import Flask
from db_communicate import load_db, add_user, save_userdb, update_state

app = Flask(__name__)
SwellDB, DataFiles = load_db()

"""Command line API for communicating with the Swell data base."""


@app.cli.command()
def hello():
    """Greet the user."""
    click.echo('Hello!')


@app.cli.command()
def viewall():
    """View entire database."""
    pretty_response = json.dumps(SwellDB, indent=2, sort_keys=True, ensure_ascii=False)
    click.echo(pretty_response)


@app.cli.command()
@click.option('--user', default="")
def viewuser(user):
    """Get the user's data set."""
    if not SwellDB.get(user):
        click.echo("Error: unknown user: %s" % user)
    else:
        pretty_response = json.dumps(SwellDB[user], indent=2, sort_keys=True, ensure_ascii=False)
        click.echo(pretty_response)


@app.cli.command()
@click.option('--user', default="")
@click.option('--pw', default="")
def adduser(user, pw):
    """Adds a user to the data base."""
    try:
        add_user(user, pw, SwellDB, DataFiles)
        click.echo("Successfully added user: %s" % user)
    except:
        "Unexpected error occurred! %s" % sys.exc_info()[0]


@app.cli.command()
@click.option('--user')
@click.option('--state')
def setuser(user, state):
    """Update a user's state."""
    if not SwellDB.get(user):
        click.echo("Error: unknown user: %s" % user)
        return
    try:
        update_state(SwellDB[user], user, state)
    except:
        click.echo("Could not update data base!")
        return
    try:
        save_userdb(SwellDB[user], user, DataFiles)
        click.echo("Successfully updated state of user: %s" % user)
    except:
        click.echo("Could not save changes to data base!")
