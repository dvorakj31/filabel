import click
import requests
import configparser
import fnmatch
import sys
import json
from colorama import Fore, Style


class GithubCom:
    """
    Auxiliary class to help operating Github API
    """

    _GH_ENDPOINT = 'https://api.github.com'

    def __init__(self, token):
        self._token = token
        self._session = requests.Session()
        self._session.headers = {'User-Agent': 'Python'}
        self._session.auth = self._token_auth

    def _token_auth(self, req):
        req.headers['Authorization'] = f'token {self._token}'
        return req

    def _get_all_pages(self, url, params=None):
        all_pages = []
        if not params:
            params = {}
        params['per_page'] = 100
        params['page'] = 1
        while True:
            resp = self._session.get(f'{url}', params=params)
            resp.raise_for_status()
            if not len(resp.json()):
                return all_pages
            all_pages.append(resp)
            params['page'] += 1

    def get_user_info(self):
        return self._session.get(self._GH_ENDPOINT + '/user')

    def get_all_prs(self, repo, state_filter, branch_filter=None):
        params = {'state': state_filter}
        url = f'{self._GH_ENDPOINT}/repos/{repo}/pulls'
        if branch_filter:
            params['base'] = branch_filter
        return self._get_all_pages(url, params)

    def _get_repo_labels(self, repo):
        return self._session.get(f'{self._GH_ENDPOINT}/repos/{repo}/labels')

    def create_label(self, repo, label_name):
        repo_labels = self._get_repo_labels(repo)
        for label in repo_labels.json():
            if label_name == label['name']:
                return repo_labels
        return self._session.post(f'{self._GH_ENDPOINT}/repos/{repo}/labels', data=json.dumps({
            'name': f'{label_name}',
            'color': 'f16a22'}))

    def set_label(self, repo, label_name, pr_num):
        return self._session.post(f'{self._GH_ENDPOINT}/repos/{repo}/issues/{pr_num}/labels', data=json.dumps(
            [label_name]))

    def delete_label_pr(self, repo, label_name, pr_num):
        return self._session.delete(f'{self._GH_ENDPOINT}/repos/{repo}/issues/{pr_num}/labels/{label_name}')

    def list_pr_files(self, repo, pr_num):
        url = f'{self._GH_ENDPOINT}/repos/{repo}/pulls/{pr_num}/files'
        return self._get_all_pages(url)

    # def pr_labels(self, repo, prnum):
    #     # TODO set auth header if you hit rate limit
    #     return sorted(l['name'] for l in self._session.get(f'https://api.github.com/repos/{repo}/pulls/{prnum}').
    #                   json()['labels'])


"""
Here starts auxiliary functions for validation of input and main functionality of this application
"""


def get_auth_conf(conf_path):
    auth_config = configparser.ConfigParser()
    auth_config.read(conf_path)
    return auth_config['github']['token']


def get_labels(labels_path):
    labels_config = configparser.ConfigParser()
    labels_config.read(labels_path)
    return labels_config['labels']


def get_invalid_reposlug(reposlugs):
    for x in reposlugs:
        if len(x.split('/', 1)) != 2 or '' in x.split('/'):
            return x
    return None


def _check_opt_in_pr_labels(opt, pr_labels):
    for x in pr_labels:
        if opt == x['name']:
            return True
    return False


def _check_rules(files, rules):
    for f in files:
        for r in rules.split('\n'):
            if fnmatch.fnmatch(f['filename'], r):
                return True
    return False


def _set_pr_label(gh, repo, pr, delete_old, labels, pr_labels):
    print_labels = {}
    for opt in sorted(labels):
        pr_files = gh.list_pr_files(repo, pr['number'])
        files = []
        for f in pr_files:
            f.raise_for_status()
            files += f.json()
        if _check_opt_in_pr_labels(opt, pr_labels):
            if not labels[opt] and delete_old:
                gh.delete_label_pr(repo, opt, pr['number']).raise_for_status()
                print_labels[opt] = Fore.RED + f'- {opt}'
            if _check_rules(files, labels[opt]):
                print_labels[opt] = f'= {opt}'
        elif _check_rules(files, labels[opt]):
            resp = gh.create_label(repo, opt)
            resp.raise_for_status()
            gh.set_label(repo, opt, pr['number']).raise_for_status()
            print_labels[opt] = Fore.GREEN + f'+ {opt}'
    return print_labels


def _label_prs(gh, repo, prs, delete_old, labels):
    for pr in prs:
        pr_line = '  ' + Style.BRIGHT + 'PR' + Style.RESET_ALL + f' {pr["html_url"]} - '
        try:
            print_labels = _set_pr_label(gh, repo, pr, delete_old, labels, pr['labels'])
            s_labels = sorted(print_labels)
            click.echo(pr_line + Style.BRIGHT + Fore.GREEN + 'OK' + Style.RESET_ALL)
            for label in s_labels:
                click.echo(' ' * 4 + print_labels[label] + Style.RESET_ALL)
        except requests.HTTPError:
            click.echo(pr_line + Style.BRIGHT + Fore.RED + 'FAIL' + Style.RESET_ALL)


def label_data(gh, state, branch, delete_old, reposlugs, labels):
    for repo in reposlugs:
        repo_line = Style.BRIGHT + 'REPO' + Style.RESET_ALL + f' {repo}' + ' - ' + Style.BRIGHT
        try:
            prs = gh.get_all_prs(repo, state, branch)
            pr_list = []
            for pr in prs:
                pr.raise_for_status()
                pr_list += pr.json()
            click.echo(repo_line + Fore.GREEN + 'OK' + Style.RESET_ALL)
            _label_prs(gh, repo, pr_list, delete_old, labels)
        except requests.HTTPError:
            click.echo(repo_line + Fore.RED + 'FAIL' + Style.RESET_ALL)


@click.command()
@click.option('-s', '--state', help='Filter pulls by state.', type=click.Choice(['open', 'closed', 'all']),
              default='open', show_default=open)
@click.option('--delete-old/--no-delete-old', '-d/-D', help='Delete labels that do not match anymore.', default=True,
              show_default=True)
@click.option('-b', '--base', 'branch', help='Filter pulls by base (PR target) branch name.', metavar='BRANCH')
@click.option('-a', '--config-auth', help='File with authorization configuration.', metavar='FILENAME')
@click.option('-l', '--config-labels', help='File with labels configuration.', metavar='FILENAME')
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
        token = get_auth_conf(config_auth)
    except(KeyError, configparser.Error):
        click.echo('Auth configuration not usable!', err=True)
        sys.exit(1)
    try:
        labels = get_labels(config_labels)
    except(KeyError, configparser.Error):
        click.echo('Labels configuration not usable!', err=True)
        sys.exit(1)
    invalid_reposlug = get_invalid_reposlug(reposlugs)
    if invalid_reposlug:
        click.echo(f'Reposlug {invalid_reposlug} not valid!', err=True)
        sys.exit(1)
    gh = GithubCom(token)
    label_data(gh, state, branch, delete_old, reposlugs, labels)


if __name__ == '__main__':
    main()
