import os
import click
import json
from flask import Blueprint
from flask.cli import with_appcontext
from application import APP_ROOT
from .fixture_importer import import_fixture

# Blueprint Configuration
cli_bp = Blueprint('cli_bp', __name__, cli_group='kss')

fixtures_path = os.path.join(APP_ROOT, 'fixtures')


@with_appcontext
@cli_bp.cli.command('fixtures')
def insert_fixtures():
    fixture_disct = {}

    # r=root, d=directories, f = files
    for r, d, f in os.walk(fixtures_path):
        for file in f:
            if ".json" in file:
                fixture_disct.update({file: os.path.join(r, file)})

    # key is filename and value is file path
    for key, value in fixture_disct.items():
        click.echo('Importing: %s' % key)
        file = open(value, "r")
        fixture = json.loads(file.read())
        # Debug file content with pretty print
        # click.echo(json.dumps(fixture, indent=4, sort_keys=True))
        import_fixture(fixture)
