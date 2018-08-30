"""alie cli tests."""

from click.testing import CliRunner
from os import environ
import pytest

from alie import cli

def test_main(tmpdir):
    """Sample test for main command."""
    runner = CliRunner()
    environ['ALIE_JSON_PATH'] = tmpdir.join('json').strpath
    environ['ALIE_ALIASES_PATH'] = tmpdir.join('aliases').strpath

    for i in range(10):
        params = [f'test_quick_{i}', 'echo']
        result = runner.invoke(cli.main, params)
        assert 'CREATED' in result.output

    params = ['test_quick_0']
    result = runner.invoke(cli.main, params)
    assert 'REMOVED' in result.output

    result = runner.invoke(cli.main, [])
    assert '[9 registered]' in result.output

    result = runner.invoke(cli.main, ['hello'])
    assert 'not registered' in result.output

    params = [f'say', 'echo "$@"', '-f']
    result = runner.invoke(cli.main, params)
    assert 'CREATED' in result.output

    result = runner.invoke(cli.main, [])
    assert 'function ' in result.output
