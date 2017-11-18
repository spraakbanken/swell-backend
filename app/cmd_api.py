import click
import json
import sys
import logging
from flask import Flask
from db_communicate import load_db, add_user, update_state
from config import C

app = Flask(__name__)
SwellDB = load_db()

# Logging is not working :(
logging.basicConfig(stream=sys.stdout)
log = logging.getLogger('swell-backend.' + __name__)

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
@click.argument('user')
def viewuser(user):
    """Get the user's data set."""
    if not SwellDB.get(user):
        click.echo("Error: unknown user: %s" % user)
    else:
        pretty_response = json.dumps(SwellDB[user][C.State], indent=2, sort_keys=True, ensure_ascii=False)
        print(pretty_response)


@app.cli.command()
@click.argument('user')
@click.argument('password')
@click.argument('input', type=click.File('r'))
def adduser(user, password, input):
    """Adds a user to the data base."""
    add_user(user, password, input.read(), SwellDB)
    click.echo("Successfully added user: %s" % user)


@app.cli.command()
@click.argument('user')
@click.argument('input', type=click.File('r'))
def setuser(user, input):
    """Update a user's state."""
    if not SwellDB.get(user):
        click.echo("Error: unknown user: %s" % user)
        return
    update_state(user, input.read(), SwellDB)
    click.echo("Successfully updated state of user: %s" % user)
