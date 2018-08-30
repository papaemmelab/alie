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
from os import getenv
import json

import click
import slugify

from alie import __version__


class Alie:

    """A class used to manage user specific configurations."""

    _settings_json = join(expanduser('~'), '.alie.json')
    _settings_aliases = join(expanduser('~'), '.alie')

    def __repr__(self):  # pragma: no cover
        """Show all configurations in `settings_json`."""
        items = list(self.read().items())
        items.sort(key=lambda i: i[1].get('is_function'))
        ret = click.style(f'[{len(items)} registered]', fg='green')
        ret = click.style(f'\nalie {ret}\n\n', fg='cyan')

        for i, j in items:
            atype = 'function' if j['is_function'] else 'alias'
            ret += click.style(f'\t{atype} ', fg='blue')
            ret += click.style(f'{i}', fg='magenta') + f'={j["target"]}\n'

        return ret

    @property
    def settings_json(self):
        """Path to json file."""
        return getenv('ALIE_JSON_PATH', self._settings_json)

    @property
    def settings_aliases(self):
        """Path to aliases file."""
        return getenv('ALIE_ALIASES_PATH', self._settings_aliases)

    def read(self):
        """Read settings.json."""
        try:
            with open(self.settings_json, 'r') as f:
                return json.load(f) or {}
        except:  # pylint: disable=W0702
            return {}

    def write(self, name, value, is_function=False):
        """Write key, value to settings.json."""
        data = self.read()

        with open(self.settings_json, 'w') as f:
            data[name] = {'target': value, 'is_function': is_function}
            json.dump(data, f, indent=4, sort_keys=True)

        self.load()
        return data

    def delete(self, name):
        """Delete alias from settings.json."""
        data = self.read()

        with open(self.settings_json, 'w') as f:
            data.pop(name, None)
            json.dump(data, f, indent=4, sort_keys=True)

        self.load()
        return data

    def load(self):
        """Write aliases and reload bash profile."""
        with open(self.settings_aliases, 'w') as f:
            for i, j in self.read().items():
                target = j['target']

                if j['is_function']:
                    f.write(f"function {i} () {{ {target} }} \n")
                else:
                    f.write(f"alias {i}='{target}'\n")


@click.command()
@click.argument('alias', required=False)
@click.argument('command', required=False, default=None)
@click.option('--is-function', '-f', is_flag=True)
@click.version_option(version=__version__)
def main(alias, command, is_function):
    """
    Register aliases.

    Pass no arguments to list aliases. Pass only the `ALIAS` to remove it.
    """
    alie = Alie()
    alias = slugify.slugify(alias or '', separator='_')
    colored = click.style(f'{alias}', fg='magenta')

    if not alias:
        msg = alie
    elif command:
        alie.write(alias, command, is_function=is_function)
        msg = click.style('CREATED ', fg='green') + f"{colored}='{command}'"
    elif alias in alie.read():
        alie.delete(alias)
        msg = click.style('REMOVED ', fg='red') + colored
        msg += f'. Use `unalias {alias}` to remove from this session.'
    else:
        msg = f'Cannot remove since alias {colored} not registered in alie.'

    click.echo(msg)
