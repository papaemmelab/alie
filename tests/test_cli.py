"""alie cli tests."""

from click.testing import CliRunner
import pytest

from alie import cli

def test_main():
    """Sample test for main command."""
    runner = CliRunner()
    params = ['test_quick', 'echo']
    result = runner.invoke(cli.main, params)
    assert 'CREATED' in result.output

    params = ['test_quick']
    result = runner.invoke(cli.main, params)
    assert 'REMOVED' in result.output
