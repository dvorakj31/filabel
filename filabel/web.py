import click
import configparser
import hashlib
import hmac
import sys
import os
import requests
import filabel.helper_functions
from filabel.github_handler import GithubCom
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def webhook_handler():
    try:
        conf = configparser.ConfigParser()
        conf.read(os.environ['FILABEL_CONFIG'].split(':'))
        token = conf['github']['token']
        secret = conf['github']['secret']
    except (configparser.Error, KeyError):
        click.echo('Wrong configuration', err=True)
        sys.exit(1)
    if request.method == 'POST':
        control_hash = 'sha1=' + hmac.HMAC(bytearray(secret, encoding='UTF-8'), request.data,
                                           digestmod=hashlib.sha1).hexdigest()
        try:
            if not hmac.compare_digest(control_hash, request.headers['X-Hub-Signature']):
                return 'Illegal operation', 403
            if request.headers['X-GitHub-Event'] == 'ping':
                return '', 200
            elif request.headers['X-GitHub-Event'] == 'pull_request' and request.json['action'] != 'labeled' and \
                    request.json['action'] != 'unlabeled':
                filabel.helper_functions.label_pr(GithubCom(token), request.json['repository']['full_name'],
                                                  request.json['pull_request'], conf['labels'])
            else:
                return '', 501
        except KeyError:
            return '', 500
        return '', 200
    else:
        try:
            conn = GithubCom(token).get_user_info()
            conn.raise_for_status()
            return render_template('index.html', username=conn.json()['login'], labels=conf['labels'])
        except (requests.HTTPError, KeyError):
            return 'Wrong server configuration', 500
