import click
import configparser
import sys
import filabel.helper_functions
from filabel.github_handler import GithubCom


@click.command()
@click.option('-s', '--state', help='Filter pulls by state.', type=click.Choice(['open', 'closed', 'all']),
              default='open', show_default=open)
@click.option('--delete-old/--no-delete-old', '-d/-D', help='Delete labels that do not match anymore.', default=True,
              show_default=True)
@click.option('-b', '--base', 'branch', help='Filter pulls by base (PR target) branch name.', metavar='BRANCH')
@click.option('-a', '--config-auth', help='File with authorization configuration.', metavar='FILENAME',
              envvar='FILABEL_CONFIG')
@click.option('-l', '--config-labels', help='File with labels configuration.', metavar='FILENAME',
              envvar='FILABEL_CONFIG')
@click.argument('reposlugs', nargs=-1)
def main(state, delete_old, branch, config_auth, config_labels, reposlugs):
    """
        CLI tool for filename-pattern-based labeling of GitHub PRs
    """
    if not config_auth:
        click.echo('Auth configuration not supplied!', err=True)
        sys.exit(1)
    if not config_labels:
        click.echo('Labels configuration not supplied!', err=True)
        sys.exit(1)
    try:
        print('config:', config_auth)
        token = filabel.helper_functions.get_auth_conf(config_auth)
    except(KeyError, configparser.Error):
        click.echo('Auth configuration not usable!', err=True)
        sys.exit(1)
    try:
        labels = filabel.helper_functions.get_labels(config_labels)
    except(KeyError, configparser.Error):
        click.echo('Labels configuration not usable!', err=True)
        sys.exit(1)
    invalid_reposlug = filabel.helper_functions.get_invalid_reposlug(reposlugs)
    if invalid_reposlug:
        click.echo(f'Reposlug {invalid_reposlug} not valid!', err=True)
        sys.exit(1)
    gh = GithubCom(token)
    filabel.helper_functions.label_data(gh, state, branch, delete_old, reposlugs, labels)
