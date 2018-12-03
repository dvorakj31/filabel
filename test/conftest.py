import os
import betamax
import pytest
from filabel.github_handler import GithubCom
from filabel import web

CASSETTES_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/cassettes')
CONFIGS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/configs')


def get_token():
    return os.environ.get('GITHUB_TOKEN', '<GH_TOKEN>')


@pytest.fixture
def github_com(betamax_session):
    github_com = GithubCom(get_token(), betamax_session)
    return github_com


@pytest.fixture
def client():
    web.app.config['TESTING'] = True
    return web.app.test_client()


with betamax.Betamax.configure() as config:
    config.cassette_library_dir = CASSETTES_PATH
    token = get_token()
    if 'GITHUB_TOKEN' in os.environ:
        config.default_cassette_options['record_mode'] = 'once'
    else:
        config.default_cassette_options['record_mode'] = 'none'
    config.define_cassette_placeholder('<GH_TOKEN>', token)
