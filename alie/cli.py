"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?
You might be tempted to import things from __main__ later, but that will
cause problems, the code will get executed twice:

    - When you run `python -m alie` python will execute
      `__main__.py` as a script. That means there won't be any
      `alie.__main__` in `sys.modules`.

    - When you import __main__ it will get executed again (as a module) because
      there's no `alie.__main__` in `sys.modules`.

Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from os.path import expanduser
from os.path import join
import subprocess
import json

import click
import slugify

from alie import __version__


class Aliaz:

    """A class used to manage user specific configurations."""

    settings_json = join(expanduser('~'), '.alie.json')
    settings_aliases = join(expanduser('~'), '.alie')

    def __repr__(self):  # pragma: no cover
        """Show all configurations in `settings_json`."""
        return f'Aliases({self.read()})'

    def read(self):
        """Read settings.json."""
        try:
            with open(self.settings_json, 'r') as f:
                return json.load(f) or {}
        except:  # pylint: disable=W0702
            return {}

    def write(self, name, value):
        """Write key, value to settings.json."""
        with open(self.settings_json, 'w') as f:
            data = self.read()
            data[name] = value
            json.dump(data, f, indent=4, sort_keys=True)

        self.load()
        return data

    def delete(self, name):
        """Delete alias from settings.json."""
        with open(self.settings_json, 'w') as f:
            data = self.read()
            data.pop(name, None)
            json.dump(data, f, indent=4, sort_keys=True)

        self.load()
        return data

    def load(self):
        """Write aliases and reload bash profile."""
        with open(self.settings_aliases, 'w') as f:
            for i, j in self.read().items():
                f.write(f"alias {i}='{j}'")

        command = ['bash', '-c', f'source {self.settings_aliases}']
        subprocess.check_call(command)


@click.command()
@click.argument('alias', required=True)
@click.argument('command', required=False, default=None)
@click.version_option(version=__version__)
def main(alias, command):
    """
    Register or remove aliases.

    add: alie hello 'echo hello'
    remove: alie hello

    Please add to your bash profile: `source ~/.alie`.
    """
    alie = Aliaz()
    alias = slugify.slugify(alias, separator='_')

    if command:
        alie.write(alias, command)
        msg = click.style(f'CREATED {alias}: ', fg='green')
    else:
        alie.delete(alias)
        msg = click.style(f'REMOVED {alias}: ', fg='red')

    click.echo(msg + f"please run 'source {alie.settings_aliases}'. ")
