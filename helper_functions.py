import requests
import fnmatch
from colorama import Fore, Style
import configparser
import click


"""
Here starts auxiliary functions for validation of input and main functionality of the filabel application
"""


def get_auth_conf(conf_path):
    auth_config = configparser.ConfigParser()
    auth_config.read(conf_path.split(':'))
    return auth_config['github']['token']


def get_labels(labels_path):
    labels_config = configparser.ConfigParser()
    labels_config.read(labels_path.split(':'))
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


def label_pr(gh, repo, pr, labels):
    _label_prs(gh, repo, [pr], True, labels)
