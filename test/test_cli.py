from filabel import filabel
from click.testing import CliRunner


def test_help_command():
    run = CliRunner()
    output = run.invoke(filabel.main, ['--help'])
    assert output.exit_code == 0
    assert 'Usage: main [OPTIONS] [REPOSLUGS]...' in output.output
    assert 'CLI tool for filename-pattern-based labeling of GitHub PRs' in output.output
    assert 'Options:' in output.output
    assert '-s, --state [open|closed|all]   Filter pulls by state.  [default: open]' in output.output
    assert '-d, --delete-old / -D, --no-delete-old' in output.output
    assert '                                  Delete labels that do not match anymore.' in output.output
    assert '                                  [default: True]' in output.output
    assert '  -b, --base BRANCH               Filter pulls by base (PR target) branch name' in output.output
    assert '  -a, --config-auth FILENAME      File with authorization configuration.\n  -l, --config-labels FILENAME' \
           '    File with labels configuration.\n  --help                          Show this message and exit.\n' in\
           output.output
